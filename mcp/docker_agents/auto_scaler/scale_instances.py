# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from asg_apis import modify_desired_size
from file_functions import updated_cooldown_period


# <==================================================================================================>
#                                    ADDING SERVERS
# <==================================================================================================>
def scale_up(**kwargs):
    asg_client = kwargs["asg_client"]
    asg_details = kwargs["asg_details"]
    filename = kwargs["variables"]["filename"]
    autoscale_group_name = kwargs["autoscale_group_name"]
    no_of_instances_to_add = kwargs["variables"]["no_of_instances_to_add"]

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

    print(
        f"Increasing the desired instance size of ASG: {autoscale_group_name} from {new_desired_count - 1} to {new_desired_count}")
    modify_desired_size(asg_client, updated_object)
    print("Auto Scaling completed!")

    print("Updating Cooldown TS in file...")
    updated_cooldown_period(filename)
    return


# <==================================================================================================>
#                                    REMOVING SERVERS
# <==================================================================================================>
def scale_down(**kwargs):
    asg_client = kwargs["asg_client"]
    asg_details = kwargs["asg_details"]
    filename = kwargs["variables"]["filename"]
    autoscale_group_name = kwargs["autoscale_group_name"]
    min_spot_instances = kwargs["variables"]["min_spot_instances"]
    no_of_instances_to_remove = kwargs["variables"]["no_of_instances_to_remove"]

    current_instances_in_asg = asg_details["DesiredCapacity"]
    new_desired_count = current_instances_in_asg - no_of_instances_to_remove

    if new_desired_count < min_spot_instances:
        print(f"Min instance count reached. Cannot remove more instances.")
        return

    updated_object = {
        "DesiredCapacity": new_desired_count,
        "AutoScalingGroupName": autoscale_group_name
    }

    print(
        f"Decreasing the desired instance size of ASG: {autoscale_group_name} from {new_desired_count + 1} to {new_desired_count}")
    modify_desired_size(asg_client, updated_object)
    print("Auto Scaling completed!")

    print("Updating Cooldown TS in file...")
    updated_cooldown_period(filename)
    return
