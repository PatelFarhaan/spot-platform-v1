# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import os
import sys

import boto3
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

    def get_ec2_client(self):
        try:
            ec2_client = self.session.client(self.ec2, **self.aws_config)
            return ec2_client
        except ClientError as e:
            self.connection_issue("EC2", e)


# <==================================================================================================>
#                            GET VOLUME IDS WHICH HAVE LESS THAN 1 GB SPACE LEFT
# <==================================================================================================>
def get_volume_ids_to_be_modified() -> dict:
    volume_ids = list(instance_volume_ids.values())
    response = ec2_client.describe_volumes(
        VolumeIds=volume_ids,
    )
    from pprint import pprint
    pprint(response)


# <==================================================================================================>
#                                 GET ALL VOLUME IDS IN A APPLICATION
# <==================================================================================================>
def get_all_volume_ids() -> dict:
    instance_volume_id_map = {}
    response = ec2_client.describe_volumes(
        Filters=[
            {
                "Name": "tag:Name",
                "Values": [application_name]
            },
            {
                "Name": "tag:Environment",
                "Values": [environment]
            }
        ],
    )

    for volume in response.get("Volumes"):
        attachments = volume.get("Attachments")
        if attachments[0]:
            instance_id = attachments[0].get("InstanceId")
            volume_id = attachments[0].get("VolumeId")
            if all([instance_id, volume_id]):
                instance_volume_id_map[instance_id] = volume_id

    return instance_volume_id_map


if __name__ == '__main__':
    aws_obj = AWS()
    ec2_client = aws_obj.get_ec2_client()

    application_name = os.getenv("application_name", "spot-redflag-api-lookup")
    environment = os.getenv("environment", "production")
    instance_volume_ids = get_all_volume_ids()
    volumes_to_be_modified = get_volume_ids_to_be_modified()
