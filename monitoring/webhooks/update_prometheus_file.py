# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import os
import sys
import json
import yaml
import time
import boto3
import requests
from botocore.exceptions import ClientError


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
#                                      GET ALL INSTANCES IN ASG
# <==================================================================================================>
def get_all_instances_in_asg(autoscale_group_name: str) -> list:
    aws_obj = AWS()
    asg_client = aws_obj.get_autoscale_client()
    response = asg_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[autoscale_group_name]
    )
    if response.get("AutoScalingGroups"):
        response = response["AutoScalingGroups"][0]
        instances = response.get("Instances", {})
        instance_ids = [instance["InstanceId"] for instance in instances if instance.get("InstanceId")]
        return instance_ids
    return []


# <==================================================================================================>
#                                      GET INSTANCE DETAILS
# <==================================================================================================>
def get_instance_details(aws_obj: AWS, instance_ids: list, retry=1) -> list:

    if retry > 3:
        print("Instances are not in ready state! Aborting program")
        sys.exit(0)

    ip_list = []
    ec2_client = aws_obj.get_ec2_client()
    response = ec2_client.describe_instances(InstanceIds=instance_ids)
    reservations = response.get("Reservations", {})

    for instance_obj in reservations:
        for instance in instance_obj.get("Instances", []):
            instance_id = instance.get("InstanceId")
            public_ip_address = instance.get("PublicIpAddress")

            if all([instance_id, public_ip_address]):
                ip_list.append(public_ip_address)
            else:
                print("Sleeping for 20 secs as instances are not in running state")
                time.sleep(20)
                return get_instance_details(aws_obj, instance_ids, retry + 1)
    return ip_list


# <==================================================================================================>
#                                     REMOVE ALL CURRENT INSTANCES
# <==================================================================================================>
def remove_all_current_instances():
    with open(prometheus_file_name) as rf:
        data = yaml.load(rf, Loader=yaml.FullLoader)
        for index1, sc in enumerate(data["scrape_configs"]):
            if sc.get("job_name") == "worker-metrics":
                for index2, config in enumerate(sc["static_configs"]):
                    data["scrape_configs"][index1]["static_configs"][index2][
                        "targets"] = []

    with open(prometheus_file_name, "w") as wf:
        yaml.dump(data, wf)


# <==================================================================================================>
#                              CRONTAB: UPDATE ALL CURRENT INSTANCES OF ALL ENV
# <==================================================================================================>
def update_current_instances_of_all_env() -> None:
    aws_obj = AWS()
    all_env_names = read_json(env_ins_mapping_fn)

    for asg_name in all_env_names:
        instance_ids = get_all_instances_in_asg(asg_name)
        instance_ips = get_instance_details(aws_obj, instance_ids)
        environment, application_name = get_environment_details(asg_name)

        for ip_address in instance_ips:
            with open(prometheus_file_name) as rf:
                is_launch = True
                data = yaml.load(rf, Loader=yaml.FullLoader)
                update_instance_details(data, is_launch, environment, ip_address, application_name)

            with open(prometheus_file_name, "w") as wf:
                yaml.dump(data, wf)


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
#                                             ROUTE ENDPOINT
# <==================================================================================================>
def reload_prometheus():
    requests.post('http://prometheus:9090/-/reload')


# <==================================================================================================>
#                                              READ JSON
# <==================================================================================================>
def read_json(filename):
    with open(filename, 'r') as openfile:
        data = json.load(openfile)
    return data


# <==================================================================================================>
#                                           MAIN FUNCTION
# <==================================================================================================>
if __name__ == '__main__':
    env_ins_mapping_fn = "/application/data/environment_instance_mapping.json"
    instanceid_ip_fn = "/application/data/instanceid_ip_mapping.json"
    prometheus_file_name = "/application/data/prometheus.yml"
    remove_all_current_instances()
    update_current_instances_of_all_env()
    reload_prometheus()
