# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import os
import sys
import json
import yaml
import boto3
import requests
from pprint import pprint
from flask_crontab import Crontab
from flask import Flask, request, jsonify
from botocore.exceptions import ClientError


# <==================================================================================================>
#                                          FLASK CONFIG
# <==================================================================================================>
app = Flask(__name__)
crontab = Crontab(app)


# <==================================================================================================>
#                                          AWS CLIENT
# <==================================================================================================>
class AWS(object):
    def __init__(self):
        self.ec2 = "ec2"
        self.autoscale = "autoscaling"
        self.aws_region = os.getenv("AWS_REGION")
        self.aws_profile = os.getenv("AWS_PROFILE")
        self.session = boto3.Session(profile_name=self.aws_profile)
        self.aws_config = {
            "region_name": self.aws_region
        }

    @staticmethod
    def connection_issue(client_name, e):
        print(f"Facing issues connecting to: {client_name} client")
        print(f"Code Exception is: {e.response['Error']['Code']}")
        print(f"Error Message is: {e.response['Error']['Message']}")
        print(f"Status Code is: {e.response['ResponseMetadata']['HTTPStatusCode']}")
        sys.exit(1)

    def get_autoscale_client(self):
        try:
            as_client = self.session.client(self.autoscale, **self.aws_config)
            return as_client
        except ClientError as e:
            self.connection_issue("Autoscaling", e)

    def get_ec2_client(self):
        try:
            ec2_client = self.session.client(self.ec2, **self.aws_config)
            return ec2_client
        except ClientError as e:
            self.connection_issue("EC2", e)


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
#                                     GET INSTANCE PUBLIC IP ADDRESS
# <==================================================================================================>
def get_instance_public_ip(instance_id):
    print("Describe instance: ", instance_id)
    aws_obj = AWS()
    ec2_client = aws_obj.get_ec2_client()
    response = ec2_client.describe_instances(
        InstanceIds=[instance_id]
    )
    ipv4_address = response["Reservations"][0]["Instances"][0]["PublicIpAddress"]
    return ipv4_address


# <==================================================================================================>
#                                      GET INSTANCE ENVIRONMENT
# <==================================================================================================>
def get_environment_details(asg_name):
    data = read_json(env_ins_mapping_fn)

    if data.get(asg_name):
        return data[asg_name][0], data[asg_name][1]

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

    data[asg_name] = [env, app_name]
    save_json(env_ins_mapping_fn, data)
    return env, app_name


# <==================================================================================================>
#                                  UPDATE INSTANCE DETAILS IN PROMETHEUS
# <==================================================================================================>
def update_instance_details(data, is_launch, environment, ipv4_address, application_name):
    for index1, sc in enumerate(data["scrape_configs"]):
        if sc.get("job_name") == "worker-metrics":
            for index2, config in enumerate(sc["static_configs"]):
                if config.get("labels", {}).get("environment") == environment and \
                        config.get("labels", {}).get("application") == application_name:
                    if is_launch:
                        if f"{ipv4_address}:9100" in data["scrape_configs"][index1]["static_configs"][index2]["targets"]:
                            return
                        else:
                            ip_list = [f"{ipv4_address}:9100", f"{ipv4_address}:8080", f"{ipv4_address}:9113"]
                            data["scrape_configs"][index1]["static_configs"][index2]["targets"].extend(ip_list)
                            return
                    else:
                        if f"{ipv4_address}:9100" not in data["scrape_configs"][index1]["static_configs"][index2]["targets"]:
                            return
                        data["scrape_configs"][index1]["static_configs"][index2]["targets"].remove(
                            f"{ipv4_address}:9100")
                        data["scrape_configs"][index1]["static_configs"][index2]["targets"].remove(
                            f"{ipv4_address}:8080")
                        data["scrape_configs"][index1]["static_configs"][index2]["targets"].remove(
                            f"{ipv4_address}:9113")
                        return

            new_app_entry = {
                'labels':
                    {
                        'application': application_name,
                        'environment': environment
                    },
                'targets': [
                    f"{ipv4_address}:9100",
                    f"{ipv4_address}:8080"
                    f"{ipv4_address}:9113"
                ]
            }
            sc["static_configs"].append(new_app_entry)


# <==================================================================================================>
#                                    CHECK IF INSTANCE IS PRESENT IN JSON
# <==================================================================================================>
def check_instance_is_present(instance_id, launch):
    data = read_json(instanceid_ip_fn)
    if launch:
        if instance_id in data:
            return True
    else:
        if instance_id not in data:
            return True
    return False


# <==================================================================================================>
#                                    SAVE INSTANCE IP ADDRESS IN JSON
# <==================================================================================================>
def save_instance_ip_mapping(instance_id, save_object):
    data = read_json(instanceid_ip_fn)
    data[instance_id] = save_object
    save_json(instanceid_ip_fn, data)


# <==================================================================================================>
#                                          UPDATE PROMETHEUS FILE
# <==================================================================================================>
def update_prometheus_file(data):
    is_launch, instance_id, asg_name = is_instance_launching(data)

    if check_instance_is_present(instance_id, is_launch):
        return jsonify({}), 200

    if is_launch:
        environment, application_name = get_environment_details(asg_name)
        ipv4_address = get_instance_public_ip(instance_id)
        save_obj = {
            "environment": environment,
            "ipv4_address": ipv4_address,
            "application_name": application_name
        }
        save_instance_ip_mapping(instance_id, save_obj)
    else:
        data = read_json(instanceid_ip_fn)
        instance_details = data.pop(instance_id)
        environment = instance_details["environment"]
        ipv4_address = instance_details["ipv4_address"]
        application_name = instance_details["application_name"]
        save_json(instanceid_ip_fn, data)

    with open(prometheus_file_name) as rf:
        data = yaml.load(rf, Loader=yaml.FullLoader)
        update_instance_details(data, is_launch, environment, ipv4_address, application_name)

    with open(prometheus_file_name, "w") as wf:
        yaml.dump(data, wf)


# <==================================================================================================>
#                                          SNS NOTIFICATION
# <==================================================================================================>
@app.route("/webhook/instance-modification", methods=["POST"])
def sns_notification():
    data = json.loads(request.get_data())
    pprint(f"\n\nData -> {data}\n\n")
    update_prometheus_file(data)
    reload_prometheus()
    return jsonify({}), 200


# <==================================================================================================>
#                                          ROUTE ENDPOINT
# <==================================================================================================>
def reload_prometheus():
    requests.post('http://prometheus:9090/-/reload')


# <==================================================================================================>
#                                          ROUTE ENDPOINT
# <==================================================================================================>
@app.route("/webhook/server-health")
def health_check():
    return jsonify({"status": "OK"})


# <==================================================================================================>
#                                          READ JSON
# <==================================================================================================>
def read_json(filename):
    with open(filename, 'r') as openfile:
        data = json.load(openfile)
    return data


# <==================================================================================================>
#                                          SAVE JSON
# <==================================================================================================>
def save_json(filename, data):
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4)


# <==================================================================================================>
#                                         MAIN FUNCTION
# <==================================================================================================>
if __name__ == '__main__':
    env_ins_mapping_fn = "/application/data/environment_instance_mapping.json"
    instanceid_ip_fn = "/application/data/instanceid_ip_mapping.json"
    prometheus_file_name = "/application/data/prometheus.yml"
    app.run(host="0.0.0.0", port=5000)
