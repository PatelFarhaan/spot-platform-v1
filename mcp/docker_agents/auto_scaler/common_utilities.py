# <==================================================================================================>
#                                            IMPORTS
# <==================================================================================================>
import sys
from datetime import datetime, timedelta

from dateutil import parser

from asg_apis import get_asg_names, get_asg_details
from file_functions import read_json_file, save_json_file, create_a_file_if_does_not_exists
from scale_instances import scale_up


# <==================================================================================================>
#                                         INITIAL CHECKS
# <==================================================================================================>
def perform_initial_checks(**kwargs):
    """
    This function will check if the OD and Spot asg name is present
    This will also retrive the asg names every x mins as mentioned in the payload so the names is always up to date
    """
    filename = kwargs["filename"]
    variables = kwargs["variables"]
    asg_client = kwargs["asg_client"]
    environment = kwargs["environment"]
    application = kwargs["application"]

    create_a_file_if_does_not_exists(filename)
    content = read_json_file(filename)

    if not all(key in content for key in ["od_asg_name", "spot_asg_name"]):
        cool_down_period_mins = 5
        asg_names_update_mins = 15
        od_asg_name, spot_asg_name = get_asg_names(asg_client, application, environment)

        content["application"] = application
        content["environment"] = environment
        content["od_asg_name"] = od_asg_name
        content["spot_asg_name"] = spot_asg_name
        content["cool_down_period_mins"] = cool_down_period_mins
        content["update_asg_names_in_mins"] = asg_names_update_mins
        content["cool_down_period_ts"] = str(datetime.utcnow() + timedelta(minutes=cool_down_period_mins))
        content["asg_names_update_ts"] = str(datetime.utcnow() + timedelta(minutes=asg_names_update_mins))
        save_json_file(filename, content)

    asg_names_update_ts = content["asg_names_update_ts"]
    if timestamp_has_expired(asg_names_update_ts):
        print("Checking if Asg names has changed...")

        asg_names_update_mins = 15
        content["asg_names_update_ts"] = str(datetime.utcnow() + timedelta(minutes=asg_names_update_mins))
        save_json_file(filename, content)

    min_instances_kwargs = {
        "content": content,
        "variables": variables,
        "asg_client": asg_client
    }

    cool_down_period_ts = content["cool_down_period_ts"]
    print("Checking if Cooldown period is over...")
    if not timestamp_has_expired(cool_down_period_ts):
        string_to_dt = parser.parse(cool_down_period_ts)
        will_expire_at = string_to_dt.strftime("%Y-%m-%d %H:%M:%S%z")
        print(f"Cooldown period will expire at: {will_expire_at}. ASG cannot be modified!")
        sys.exit(0)

    asg_details = satisfy_min_no_of_instances(**min_instances_kwargs)
    if asg_details == "asg_modified":
        # If the ASG is updated to satisfy min no of instances, the abort the program as asg should only be updated once
        print("ASG updated to satisfy minimum number of instances")
        sys.exit(0)

    print("Cooldown period is over, ASG can be modified!")
    return asg_details


# <==================================================================================================>
#                               CHECK IF THE MIN NO OF OD AND SPOT IS SATISFIED
# <==================================================================================================>
def satisfy_min_no_of_instances(**kwargs):
    asg_client = kwargs["asg_client"]
    od_asg_name = kwargs["content"]["od_asg_name"]
    spot_asg_name = kwargs["content"]["spot_asg_name"]
    min_od_instances = kwargs["variables"]["min_od_instances"]
    min_spot_instances = kwargs["variables"]["min_spot_instances"]

    od_asg_details = get_asg_details(asg_client, od_asg_name)
    spot_asg_details = get_asg_details(asg_client, spot_asg_name)

    current_od_instances = od_asg_details["DesiredCapacity"]
    current_spot_instances = spot_asg_details["DesiredCapacity"]

    modified_asg = False
    if current_od_instances < min_od_instances:
        modified_asg = True
        scaling_kwargs = dict()
        scaling_kwargs["asg_client"] = asg_client
        scaling_kwargs["asg_details"] = od_asg_details
        scaling_kwargs["variables"] = kwargs["variables"]
        scaling_kwargs["autoscale_group_name"] = od_asg_name
        scaling_kwargs["variables"]["no_of_instances_to_add"] = min_od_instances - current_od_instances
        scale_up(**scaling_kwargs)

    if current_spot_instances < min_spot_instances:
        modified_asg = True
        scaling_kwargs = dict()
        scaling_kwargs["asg_client"] = asg_client
        scaling_kwargs["asg_details"] = spot_asg_details
        scaling_kwargs["variables"] = kwargs["variables"]
        scaling_kwargs["autoscale_group_name"] = spot_asg_name
        scaling_kwargs["variables"]["no_of_instances_to_add"] = min_spot_instances - current_spot_instances
        scale_up(**scaling_kwargs)

    if modified_asg:
        return "asg_modified"
    return spot_asg_details


# <==================================================================================================>
#                                  CHECK IF TIMESTAMP HAS EXPIRED
# <==================================================================================================>
def timestamp_has_expired(timestamp):
    asg_timestamp = parser.parse(timestamp)
    if datetime.utcnow() > asg_timestamp:
        return True
    return False

