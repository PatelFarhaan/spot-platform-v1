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
create_aws_credentials_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "access_key": {
            "type": "string",
        },
        "secret_key": {
            "type": "string",
        }
    },
    "required": ["name", "access_key", "secret_key"],
    "additionalProperties": False
}


def validate_create_aws_credentials_schema(data):
    try:
        validate(instance=data, schema=create_aws_credentials_schema)
    except ValidationError as e:
        abort(400, description=e.message)
    except SchemaError as e:
        abort(400, description=e.message)
    return data
