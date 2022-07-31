# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from flask import abort
from jsonschema import validate
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError

# <==================================================================================================>
#                                     REGISTER SCHEMA VALIDATION
# <==================================================================================================>
register_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
        },
        "last_name": {
            "type": "string"
        },
        "company": {
            "type": "string"
        },
        "position": {
            "type": "string"
        },
        "password": {
            "type": "string",
            "minLength": 8
        },
        "email": {
            "type": "string",
            "format": "email"
        }
    },
    "required": ["first_name", "last_name", "email", "password", "company", "position"],
    "additionalProperties": False
}


def validate_register_schema(data):
    try:
        validate(instance=data, schema=register_schema)
    except ValidationError as e:
        abort(400, description=e.message)
    except SchemaError as e:
        abort(400, description=e.message)
    return data
