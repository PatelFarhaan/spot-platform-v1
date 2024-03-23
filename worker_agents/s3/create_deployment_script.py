import json

with open("./deployment.sh", "w") as file_write:
    export_vars = ""
    data = json.load(open("./deployment.json"))

    for key, value in data.items():
        if key == "CLIENT_APP_IMAGE":
            export_vars += f"export {key}=${{AWS_ECR_ID}}/${{AWS_ECR_REPO_NAME}}:{value}\n"
        else:
            export_vars += f"export {key}={value}\n"

    content = f"""#!/bin/bash
    
set -e -x
{export_vars}"""

    file_write.write(content)
