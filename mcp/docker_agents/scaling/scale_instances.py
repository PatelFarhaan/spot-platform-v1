# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from asg_apis import modify_desired_size


# <==================================================================================================>
#                                    ADDING SERVERS
# <==================================================================================================>
def scale_up(**kwargs):
    asg_client = kwargs["asg_client"]
    asg_details = kwargs["asg_details"]
    autoscale_group_name = kwargs["autoscale_group_name"]

    no_of_instances_to_add = 1
    max_instances_limit_in_asg = asg_details["MaxSize"]
    current_instances_in_asg = asg_details["DesiredCapacity"]
    new_desired_count = current_instances_in_asg + no_of_instances_to_add

    if new_desired_count > max_instances_limit_in_asg:
        print(f"Max instance count reached. Cannot add more instances.")
        return

    updated_object = {
        "DesiredCapacity": new_desired_count,
        "AutoScalingGroupName": autoscale_group_name
    }

    print(f"Increasing the desired instance size of ASG from {new_desired_count - 1} to {new_desired_count}")
    modify_desired_size(asg_client, updated_object)
    print("Auto Scaling completed!")
    return


# <==================================================================================================>
#                                    REMOVING SERVERS
# <==================================================================================================>
def scale_down(**kwargs):
    asg_client = kwargs["asg_client"]
    asg_details = kwargs["asg_details"]
    autoscale_group_name = kwargs["autoscale_group_name"]

    no_of_instances_to_remove = 1
    min_instances_limit_in_asg = asg_details["MinSize"]
    current_instances_in_asg = asg_details["DesiredCapacity"]
    new_desired_count = current_instances_in_asg - no_of_instances_to_remove

    if new_desired_count < min_instances_limit_in_asg:
        print(f"Min instance count reached. Cannot remove more instances.")
        return

    updated_object = {
        "DesiredCapacity": new_desired_count,
        "AutoScalingGroupName": autoscale_group_name
    }

    print(f"Decreasing the desired instance size of ASG from {new_desired_count + 1} to {new_desired_count}")
    modify_desired_size(asg_client, updated_object)
    print("Auto Scaling completed!")
    return
