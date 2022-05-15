# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
from aws_services import AWS


# <==================================================================================================>
#                                     GET INSTANCE PUBLIC IP ADDRESS
# <==================================================================================================>
def get_instance_public_ip(instance_id):
    print("DEBUG: Describe instance: ", instance_id)
    aws_obj = AWS()
    ec2_client = aws_obj.get_ec2_client()
    response = ec2_client.describe_instances(
        InstanceIds=[instance_id]
    )
    ipv4_address = response["Reservations"][0]["Instances"][0]["PublicIpAddress"]
    return ipv4_address
