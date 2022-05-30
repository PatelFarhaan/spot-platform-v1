# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import os
import sys
import requests
from aws_services import AWS
from scale_instances import scale_up, scale_down
from common_utilities import perform_initial_checks


# <==================================================================================================>
#                                       GET CPU FOR AN APPLICATION
# <==================================================================================================>
def get_cpu() -> float:
    query = f"""
        100 - (avg(rate(node_cpu_seconds_total{{{promql_params},mode="idle"}}[2m])) * 100)
    """
    response = requests.get(prometheus_url + '/api/v1/query',
                            params={'query': query})
    avg_cpu = response.json()["data"]["result"][0]["value"][1]
    print(f"Current Avg CPU: {avg_cpu}")
    return float(avg_cpu)


# <==================================================================================================>
#                                       GET MEMORY FOR AN APPLICATION
# <==================================================================================================>
def get_memory() -> float:
    query = f"""
        sum((1 - (node_memory_MemAvailable_bytes{{{promql_params}}} / 
        (node_memory_MemTotal_bytes{{{promql_params}}})))* 100)
    """
    response = requests.get(prometheus_url + '/api/v1/query',
                            params={'query': query})
    avg_memory = response.json()["data"]["result"][0]["value"][1]
    print(f"Current Avg Memory: {avg_memory}")
    return float(avg_memory)


# <==================================================================================================>
#                                          MAIN CALLING FUNCTION
# <==================================================================================================>
if __name__ == '__main__':
    # Defining all the environemntal variables
    aws_region = os.getenv("aws_region")
    environment = os.getenv("environment")
    application = os.getenv("application")
    prometheus_url = os.getenv("prometheus_url")
    min_od_instances = int(os.getenv("min_od_instances"))
    min_spot_instances = int(os.getenv("min_spot_instances"))
    cpu_scale_up_threshold = int(os.getenv("cpu_scale_up_threshold"))
    cpu_scale_down_threshold = int(os.getenv("cpu_scale_down_threshold"))
    memory_scale_up_threshold = int(os.getenv("memory_scale_up_threshold"))
    memory_scale_down_threshold = int(os.getenv("memory_scale_down_threshold"))

    variables = dict()
    variables["aws_region"] = aws_region
    variables["environment"] = environment
    variables["application"] = application
    variables["prometheus_url"] = prometheus_url
    variables["min_od_instances"] = min_od_instances
    variables["min_spot_instances"] = min_spot_instances
    variables["cpu_scale_up_threshold"] = cpu_scale_up_threshold
    variables["cpu_scale_down_threshold"] = cpu_scale_down_threshold
    variables["memory_scale_up_threshold"] = memory_scale_up_threshold
    variables["memory_scale_down_threshold"] = memory_scale_down_threshold

    asg_scale_up = asg_scale_down = False
    filename = f"{application}_{environment}.json"

    # Aborting the program if any environemntal variable is missing
    for key, value in variables.items():
        if value is None:
            print(f"Reauired params: {key} is None!!!")
            sys.exit(1)

    # Defining promql pramas for application and encironment
    promql_params = f'application="{application}", environment="{environment}"'

    # Initializing AWS SDK
    aws_obj = AWS()
    asg_client = aws_obj.get_autoscale_client()

    # Getting current CPU and Memory
    cpu = get_cpu()
    memory = get_memory()

    # Checking if asg names is present in the json file
    intial_check_kwargs = {
        "filename": filename,
        "variables": variables,
        "asg_client": asg_client,
        "environment": environment,
        "application": application
    }

    spot_asg_details = perform_initial_checks(**intial_check_kwargs)

    # Defining a HM of scale up and down metrics
    scale_up_metrics_hm = {
        cpu: cpu_scale_up_threshold,
        memory: memory_scale_up_threshold
    }

    scale_down_metrics_hm = {
        cpu: cpu_scale_down_threshold,
        memory: memory_scale_down_threshold
    }

    # Checking if the current environment resource usage is greater than SU threshold: If YES, it needs to scale up
    for current_metric, scale_up_threshold in scale_up_metrics_hm.items():
        if current_metric > scale_up_threshold:
            asg_scale_up = True

    # Checking if the current environment resource usage is less than SD threshold: If YES, it needs to scale down
    for current_metric, scale_down_threshold in scale_down_metrics_hm.items():
        if current_metric < scale_down_threshold:
            asg_scale_down = True

    if asg_scale_up:
        scaling_kwargs = dict()
        scaling_kwargs["asg_client"] = asg_client
        scaling_kwargs["asg_details"] = spot_asg_details
        scaling_kwargs["autoscale_group_name"] = spot_asg_details["AutoScalingGroupName"]
        scale_up(**scaling_kwargs)
    elif asg_scale_down:
        scaling_kwargs = dict()
        scaling_kwargs["asg_client"] = asg_client
        scaling_kwargs["asg_details"] = spot_asg_details
        scaling_kwargs["autoscale_group_name"] = spot_asg_details["AutoScalingGroupName"]
        scale_down(**scaling_kwargs)
