# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import sys
import boto3
import shutil
import requests
from datetime import datetime
from botocore.exceptions import ClientError


# <==================================================================================================>
#                                          AWS CLIENT
# <==================================================================================================>
class AWS(object):
    def __init__(self):
        self.autoscale = "autoscaling"
        self.aws_config = {
            "region_name": aws_region
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


# <==================================================================================================>
#                                          PRINT CURRENT DATETIME
# <==================================================================================================>
def get_current_dt():
    now = datetime.now()
    dt_string = now.strftime("%b %d %Y, %H:%M:%S")
    return dt_string


# <==================================================================================================>
#                                          ANALYZING DISK SIZE
# <==================================================================================================>
def is_disk_full():
    total, used, free = shutil.disk_usage("/")
    _free = free // (2 ** 30)

    if _free <= free_disk_threshold_gb:
        log_obj["disk_full"] = True
        log_obj["remaining"] = f"{_free} GB"
        return True

    log_obj["disk_full"] = False
    log_obj["remaining"] = f"{_free} GB"
    print(log_obj)
    sys.exit(0)


# <==================================================================================================>
#                                           GET INSTANCE ID
# <==================================================================================================>
def get_instance_id():
    url = "http://169.254.169.254/latest/meta-data/instance-id"
    resp = requests.get(url)
    return resp.text


# <==================================================================================================>
#                                           GET AWS REGION
# <==================================================================================================>
def get_aws_region():
    url = "http://169.254.169.254/latest/meta-data/placement/availability-zone"
    resp = requests.get(url)
    return resp.text[:-1]


# <==================================================================================================>
#                                         MARK INSTANCE AS UNHEALTHY
# <==================================================================================================>
def mark_instance_as_unhealthy():
    instance_id = get_instance_id()
    response = asg_obj.set_instance_health(
        InstanceId=instance_id,
        HealthStatus="Unhealthy"
    )
    log_obj["unhealthy_api_response"] = response


# <==================================================================================================>
#                                          MAIN CALLING FUNCTION
# <==================================================================================================>
if __name__ == '__main__':
    log_obj = {}
    log_obj["instance_id"] = get_instance_id()
    log_obj["current_dt"] = get_current_dt()
    free_disk_threshold_gb = 1
    _result = is_disk_full()
    aws_region = get_aws_region()
    aws = AWS()
    asg_obj = aws.get_autoscale_client()
    mark_instance_as_unhealthy()
    print(log_obj)
