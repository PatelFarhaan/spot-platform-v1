# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from flask import abort
from jsonschema import validate
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError

# <==================================================================================================>
#                                  CREATE APPLICATION SCHEMA VALIDATION
# <==================================================================================================>
create_application_schema = {
    "type": "object",
    "properties": {
        "tags": {
            "type": "object",
        },
        "od_config": {
            "type": "object",
        },
        "spot_config": {
            "type": "object",
        },
        "security_gruops": {
            "type": "object",
        },
        "ebs_volume_size": {
            "type": "number",
        },
        "app_name": {
            "type": "string",
        },
        "iam_role": {
            "type": "string",
        },
        "aws_region": {
            "type": "string",
        },
        "ssh_key_name": {
            "type": "string",
        },
        "aws_ecr_acc_id": {
            "type": "string",
        },
        "environment": {
            "type": "string",
        },
    },
    "required": ["tags", "od_config", "spot_config", "security_gruops", "company",
                 "ebs_volume_size", "app_name", "iam_role", "aws_region", "ssh_key_name",
                 "aws_ecr_acc_id", "environment"],
    "additionalProperties": False
}


def validate_create_application_schema(data):
    try:
        validate(instance=data, schema=create_application_schema)
    except ValidationError as e:
        abort(400, description=e.message)
    except SchemaError as e:
        abort(400, description=e.message)
    return {'result': True, 'data': data}
