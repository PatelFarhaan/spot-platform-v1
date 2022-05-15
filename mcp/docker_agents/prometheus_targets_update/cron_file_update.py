# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import os
from aws_services import AWS
from file_functions import read_json, save_json
from common_functions import get_instance_public_ip


# <==================================================================================================>
#                                      DOWNLOAD ALB FILE FROM S3
# <==================================================================================================>
def download_alb_file_from_s3():
    os.system(f"cd {download_path} && aws s3 cp s3://spot-platform/docker-agents/{alb_filename} ./")


# <==================================================================================================>
#                                      GET ALL ALB LINKS
# <==================================================================================================>
def get_alb_links():
    alb_data = read_json(f"{download_path}/{alb_filename}")
    return list(alb_data.keys())


# <==================================================================================================>
#                                          GET ALB TAGS
# <==================================================================================================>
def get_instances_ip(alb_arn):
    instances = []
    tg_response = alb_obj.describe_target_groups(LoadBalancerArn=alb_arn)
    target_groups = [i["TargetGroupArn"] for i in tg_response["TargetGroups"]]

    for tg in target_groups:
        ins_response = alb_obj.describe_target_health(TargetGroupArn=tg)
        instance_ids = [j["Target"]["Id"] for j in ins_response["TargetHealthDescriptions"]]
        for instance_id in instance_ids:
            ip = get_instance_public_ip(instance_id)
            instances.append(ip)
    return instances


# <==================================================================================================>
#                                          GET ALB DETAILS
# <==================================================================================================>
def get_targets_data():
    all_targets = []

    response = alb_obj.describe_tags(
        ResourceArns=alb_links
    )
    for i in response["TagDescriptions"]:
        env = app = None
        alb_arn = i["ResourceArn"]
        for tag in i["Tags"]:
            if tag["Key"] == "Environment":
                env = tag["Value"]
            elif tag["Key"] == "Application":
                app = tag["Value"]

        instance_metadata_list = []
        instances = get_instances_ip(alb_arn)
        for ipv4_address in instances:
            instance_ips = [
                f"{ipv4_address}:8080",
                f"{ipv4_address}:9100",
                f"{ipv4_address}:9113",
                f"{ipv4_address}:4040"
            ]
            instance_metadata_list.extend(instance_ips)

        target = {
            "targets": instance_metadata_list,
            "labels": {
                "environment": env,
                "application": app
            }
        }
        all_targets.append(target)
    return all_targets


# <==================================================================================================>
#                                      MAIN FUNCTION
# <==================================================================================================>
if __name__ == '__main__':
    aws = AWS()
    download_path = "/tmp"
    alb_filename = "alb_links.json"
    targets_filename = "/data/app_nodes.json"

    alb_obj = aws.get_alb_client()
    download_alb_file_from_s3()
    alb_links = get_alb_links()
    targets = get_targets_data()
    save_json(targets_filename, targets)
