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
        self.autoscale = "autoscaling"
        self.aws_region = os.getenv("aws_region")
        self.aws_config = {
            "region_name": self.aws_region,
        }

    @staticmethod
    def exception_block(e, client_name):
        print(f"{client_name} client is None")
        print(f"Code Exception is: {e.response['Error']['Code']}")
        print(f"Error Message is: {e.response['Error']['Message']}")
        print(f"Status Code is: {e.response['ResponseMetadata']['HTTPStatusCode']}")
        sys.exit(1)

    def get_autoscale_client(self):
        try:
            as_client = boto3.client(self.autoscale, **self.aws_config)
            return as_client
        except ClientError as e:
            self.exception_block(e, "Autoscale")
