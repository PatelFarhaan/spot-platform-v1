# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import os
import sys
import json
import jenkins
import xmltodict


# <==================================================================================================>
#                                          GET BASE TEMPLATE
# <==================================================================================================>
def get_base_template(name: str) -> json:
    base_template_for_spot = server.get_job_config(name)
    if base_template_for_spot:
        str_data = json.dumps(xmltodict.parse(base_template_for_spot))
        return json.loads(str_data)
    else:
        print(f"Base template not found: {base_template_for_spot}")
        sys.exit(1)


# <==================================================================================================>
#                                        MODIFY/UPDATE BASE TEMPLATE
# <==================================================================================================>
def modify_base_template(base_template: json, **kwargs) -> str:
    updated_string_parameter_list = []
    for string_parameter_obj in base_template["project"]["properties"]["hudson.model.ParametersDefinitionProperty"]\
            ["parameterDefinitions"]["hudson.model.StringParameterDefinition"]:
        if string_parameter_obj.get("name") == "autoscale_group_name":
            string_parameter_obj["defaultValue"] = kwargs["autoscale_group_name"]
        elif string_parameter_obj.get("name") == "od_autoscale_group_name":
            string_parameter_obj["defaultValue"] = kwargs["od_autoscale_group_name"]
        updated_string_parameter_list.append(string_parameter_obj)

    base_template["project"]["properties"]["hudson.model.ParametersDefinitionProperty"]\
        ["parameterDefinitions"]["hudson.model.StringParameterDefinition"] = updated_string_parameter_list
    return base_template


# <==================================================================================================>
#                                       CONVERT TEMPLATE TO XML CONFIG
# <==================================================================================================>
def convert_template_to_jenkins_xml(json_data: json) -> str:
    response = xmltodict.unparse(json_data)
    return response


# <==================================================================================================>
#                                         CREATE A NEW JENKINS JOB
# <==================================================================================================>
def create_new_job(job_name, job_config):
    try:
        server.create_job(job_name, job_config)
    except Exception as e:
        print(f"There was an error creating the jenkins job: {e}")


# <==================================================================================================>
#                                          MAIN FUNCTION
# <==================================================================================================>
if __name__ == '__main__':
    new_job_name = "test"
    jenkins_base_url = os.getenv("JENKINS_BASE_URL")
    jenkins_username = os.getenv("JENKINS_USERNAME")
    jenkins_password = os.getenv("JENKINS_PASSWORD")
    base_template_name = os.getenv("JENKINS_BASE_TEMPLATE_ASG_NAME")
    platform_scaling_details = {
        "autoscale_group_name": "sample1",
        "od_autoscale_group_name": "sample2",
    }

    server = jenkins.Jenkins(jenkins_base_url,
                             username=jenkins_username,
                             password=jenkins_password)

    base_template = get_base_template(base_template_name)

    modified_template = modify_base_template(base_template, **platform_scaling_details)
    jenkins_config = convert_template_to_jenkins_xml(modified_template)

    create_new_job(new_job_name, jenkins_config)
