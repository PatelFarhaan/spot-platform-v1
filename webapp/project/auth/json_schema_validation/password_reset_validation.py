# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from flask import abort
from jsonschema import validate
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError

# <==================================================================================================>
#                                        LOGIN SCHEMA VALIDATION
# <==================================================================================================>
password_reset_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "new_password": {
            "type": "string",
            "minLength": 8
        },
        "confirm_password": {
            "type": "string",
            "minLength": 8
        },
        "secret_code": {
            "type": "string",
            "minLength": 8
        },
    },
    "required": ["email", "new_password", "confirm_password", "secret_code"],
    "additionalProperties": False
}


def validate_password_reset_schema(data):
    try:
        validate(instance=data, schema=password_reset_schema)
    except ValidationError as e:
        abort(400, description=e.message)
    except SchemaError as e:
        abort(400, description=e.message)
    return data
