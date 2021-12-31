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
        self.aws_region = os.getenv("aws_region")
        self.aws_config = {
            "region_name": self.aws_region,
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "aws_session_token": ""
        }

    def get_autoscale_client(self):
        try:
            as_client = boto3.client(self.autoscale, **self.aws_config)
            return as_client
        except ClientError as e:
            print(f"Code Exception is: {e.response['Error']['Code']}")
            print(f"Error Message is: {e.response['Error']['Message']}")
            print(f"Status Code is: {e.response['ResponseMetadata']['HTTPStatusCode']}")
            sys.exit(1)

    def get_ec2_client(self):
        try:
            ec2_client = boto3.client(self.ec2, **self.aws_config)
            return ec2_client
        except ClientError as e:
            print(f"Code Exception is: {e.response['Error']['Code']}")
            print(f"Error Message is: {e.response['Error']['Message']}")
            print(f"Status Code is: {e.response['ResponseMetadata']['HTTPStatusCode']}")
            sys.exit(1)
