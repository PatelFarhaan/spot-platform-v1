# <==================================================================================================>
#                                           IMPORTS
# <==================================================================================================>
import sys


# <==================================================================================================>
#                                    GET ASG DETAILS
# <==================================================================================================>
def get_asg_details(asg_client, autoscale_group_name: str):
    response = asg_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[autoscale_group_name]
    )
    if response.get("AutoScalingGroups"):
        response = response["AutoScalingGroups"][0]
        return response

    print(f"The ASG returned null response: {autoscale_group_name}")
    print(response)
    sys.exit(1)


# <==================================================================================================>
#                                       INCREASE/DECREASE DESIRED SIZE
# <==================================================================================================>
def modify_desired_size(asg_client, updated_object):
    print(updated_object)
    response = asg_client.update_auto_scaling_group(**updated_object)
    print(response)


# <==================================================================================================>
#                                       GET OD AND SPOT ASG NAMES
# <==================================================================================================>
def get_asg_names(asg_client, application_name, environment):
    od_asg_name = spot_asg_name = None

    response = asg_client.describe_auto_scaling_groups(
        Filters=[
            {
                "Name": "tag:Application",
                "Values": [f"{application_name}"]
            },
            {
                "Name": "tag:Environment",
                "Values": [f"{environment}"]
            },
            {
                "Name": "tag:MCP_SD",
                "Values": ["true"]
            }
        ])

    for asg in response["AutoScalingGroups"]:
        for tag in asg["Tags"]:
            if tag["Key"] == "Type" and tag["Value"] == "On-Demand":
                od_asg_name = asg["AutoScalingGroupName"]
            elif tag["Key"] == "Type" and tag["Value"] == "Spot":
                spot_asg_name = asg["AutoScalingGroupName"]

    return od_asg_name, spot_asg_name
