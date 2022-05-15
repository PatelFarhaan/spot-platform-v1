# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import json
from aws_services import AWS
from flask_crontab import Crontab
from flask import Flask, request, jsonify
from file_functions import save_json, read_json
from slack_notify import send_slack_notification
from common_functions import get_instance_public_ip


# <==================================================================================================>
#                                          FLASK CONFIG
# <==================================================================================================>
app = Flask(__name__)
crontab = Crontab(app)


# <==================================================================================================>
#                                          PARSE DATA
# <==================================================================================================>
def is_instance_launching(data):
    message = json.loads(data["Message"])
    description = message.get("Description")
    instance_id = message.get("EC2InstanceId")
    asg_name = message.get("AutoScalingGroupName")

    if description.startswith("Terminating EC2 instance"):
        return False, instance_id, asg_name
    elif description.startswith("Launching a new EC2 instance"):
        return True, instance_id, asg_name


# <==================================================================================================>
#                                      GET INSTANCE ENVIRONMENT
# <==================================================================================================>
def update_environment_details(asg_name, instance_id):
    metadata = read_json(metadata_file)
    ipv4_address = get_instance_public_ip(instance_id)

    if metadata.get(asg_name):
        print("DEBUG: Instance metadata present!!!")
        environment = metadata[asg_name]["environment"]
        application_name = metadata[asg_name]["application_name"]
        metadata[asg_name]["instances"][instance_id] = ipv4_address
        save_json(metadata_file, metadata)
        return environment, application_name, ipv4_address

    print("DEBUG: Instance metadata is not present!!!")
    aws_obj = AWS()
    env = app_name = None
    as_client = aws_obj.get_autoscale_client()
    response = as_client.describe_tags(
        Filters=[
            {
                'Name': 'auto-scaling-group',
                'Values': [asg_name]
            },
        ],
    )
    for tags in response["Tags"]:
        if tags["Key"] == "Environment":
            env = tags["Value"]
        if tags["Key"] == "Application":
            app_name = tags["Value"]

    metadata[asg_name] = {}
    metadata[asg_name]["instances"] = {}
    metadata[asg_name]["environment"] = env
    metadata[asg_name]["application_name"] = app_name
    metadata[asg_name]["instances"][instance_id] = ipv4_address
    save_json(metadata_file, metadata)
    return env, app_name, ipv4_address


# <==================================================================================================>
#                                  UPDATE PROMETHEUS FILE
# <==================================================================================================>
def update_target_file(add_target: bool, data: dict):
    target_found = False
    targets_data = read_json(targets_file)
    environment = data["environment"]
    ipv4_address = data["instance_ipv4"]
    application_name = data["application_name"]
    instance_metadata_list = [
        f"{ipv4_address}:8080",
        f"{ipv4_address}:9100",
        f"{ipv4_address}:9113",
        f"{ipv4_address}:4040"
    ]

    for index, application in enumerate(targets_data):
        if application["labels"]["application"] == application_name and \
                application["labels"]["environment"] == environment:
            if add_target:
                target_found = True
                targets_data[index]["targets"].extend(instance_metadata_list)
            else:
                for instance in instance_metadata_list:
                    if instance in targets_data[index]["targets"]:
                        targets_data[index]["targets"].remove(instance)
        break

    if add_target and not target_found:
        new_target = {
            "targets": instance_metadata_list,
            "labels": {
                "environment": environment,
                "application": application_name
            }
        }
        targets_data.append(new_target)

    save_json(targets_file, targets_data)


# <==================================================================================================>
#                                          PROCESS DATA
# <==================================================================================================>
def process_data(data):
    instance_data = dict()
    new_target, instance_id, asg_name = is_instance_launching(data)

    if new_target:
        print(f"DEBUG: A new instance is registered: {instance_id}")
        environment, application_name, ipv4_address = update_environment_details(asg_name, instance_id)
        instance_data["environment"] = environment
        instance_data["instance_ipv4"] = ipv4_address
        instance_data["application_name"] = application_name
        update_target_file(new_target, instance_data)
    else:
        metadata = read_json(metadata_file)
        if asg_name not in metadata:
            print("DEBUG: Target is not present in the config!!!")
            return

        print(f"DEBUG: An instance is getting de-registered: {instance_id}")
        environment = metadata[asg_name]["environment"]
        application_name = metadata[asg_name]["application_name"]
        ipv4_address = metadata[asg_name]["instances"][instance_id]
        metadata[asg_name]["instances"].pop(instance_id)
        save_json(metadata_file, metadata)

        instance_data["environment"] = environment
        instance_data["instance_ipv4"] = ipv4_address
        instance_data["application_name"] = application_name

        update_target_file(new_target, instance_data)


# <==================================================================================================>
#                                          SNS NOTIFICATION
# <==================================================================================================>
@app.route("/webhook/instance-modification", methods=["POST"])
def sns_notification():
    # try:
    data = json.loads(request.get_data())
    print(f"DEBUG: Data -> {data}")
    if data.get("Type") == "SubscriptionConfirmation":
        send_slack_notification(data=data)
    else:
        process_data(data)
    # except Exception as e:
    #     print(f"DEBUG: Data is: {request.get_data()}")
    #     print(f"DEBUG: Something went wrong: {e}")
    #     send_slack_notification(failed=True)
    return jsonify({}), 200


# <==================================================================================================>
#                                         MAIN FUNCTION
# <==================================================================================================>
if __name__ == '__main__':
    metadata_file = "/data/metadata.json"
    targets_file = "/data/app_nodes.json"
    app.run(host="0.0.0.0", port=5000)
