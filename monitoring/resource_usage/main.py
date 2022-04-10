import os
import sys
import json
import boto3
import psutil
import requests
from flask import Flask, request, jsonify
from botocore.exceptions import ClientError

app = Flask(__name__)


# <==================================================================================================>
#                                          AWS CLIENT
# <==================================================================================================>
class AWS(object):
    def __init__(self):
        self.ec2 = "ec2"
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.aws_profile = os.getenv("AWS_PROFILE", "eb-cli")
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


@app.route("/usage", methods=["GET"])
def get_resource_usage():
    cpu_t = int(os.getenv("CPU_THRESHOLD"))
    mem_t = int(os.getenv("MEM_THRESHOLD"))
    disk_t = int(os.getenv("DISK_THRESHOLD"))

    load1, load5, load15 = psutil.getloadavg()

    cpu_usage = round((load1 / os.cpu_count()) * 100, 4)
    mem_usage = round(psutil.virtual_memory().percent, 4)
    disk_usage = round(psutil.disk_usage(__file__).percent, 4)

    result = dict()
    result["cpu"] = {}
    result["mem"] = {}
    result["disk"] = {}

    result["cpu"]["usage"] = cpu_usage
    result["cpu"]["overloaded"] = True if cpu_usage >= cpu_t else False

    result["mem"]["usage"] = mem_usage
    result["mem"]["overloaded"] = True if mem_usage >= mem_t else False

    result["disk"]["usage"] = disk_usage
    result["disk"]["overloaded"] = True if disk_usage >= disk_t else False
    return jsonify({
        "result": True,
        "data": result
    })


@app.route("/increase-ebs-size", methods=["POST"])
def increase_ebs_size():
    def _get_ebs_details(ec2_client, volume_id):
        describe_response = ec2_client.describe_volumes(
            VolumeIds=[volume_id]
        )
        return describe_response["Volumes"][0]

    def _get_volume_metadata(ec2_client):
        data = request.get_json()
        if "volume_id" not in data:
            return jsonify({
                "result": False,
                "message": "Key 'volume_id' not found in payload"
            })

        volume_id = data["volume_id"]
        ebs_details = _get_ebs_details(ec2_client, volume_id)
        size = ebs_details["Size"]
        iops = ebs_details["Iops"]
        vol_type = ebs_details["VolumeType"]
        return volume_id, size

    ec2_client = aws_obj.get_ec2_client()
    volume_id, size = _get_volume_metadata(ec2_client)
    size = size + int(os.getenv("EBS_SIZE_INCREASE"))

    modify_volume_response = ec2_client.modify_volume(
        Size=size,
        VolumeId=volume_id
    )
    # send this to SQS and update code in TF to spin up a SQS
    message = f""
    send_slack_notification(message)
    return {}


def send_slack_notification(message):
    # Todo: Integrate block kit

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {
        "text": message,
        "channel": "#development",
        "icon_emoji": ":robot_face:",
        "username": "Spot Automation"
    }

    slack_url = os.getenv("SLACK_URL", "***REMOVED***")
    response = requests.post(slack_url,
                             headers=headers,
                             data=json.dumps(payload))
    print(response.text)


if __name__ == '__main__':
    aws_obj = AWS()
    app.run(debug=False, host="127.0.0.1", port=1111)

"vol-0e75843c11269c652"

"""
1. Submit a request
2. Send details to SQS
3. Constantly poll and error in slack if it takes more than an hour
4. Once succeded then call script to increase size manually
"""