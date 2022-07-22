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
login_schema = {
    "type": "object",
    "properties": {
        "password": {
            "type": "string",
            "minLength": 8
        },
        "email": {
            "type": "string",
            "format": "email"
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


def validate_login_schema(data):
    try:
        validate(instance=data, schema=login_schema)
    except ValidationError as e:
        abort(400, description=e.message)
    except SchemaError as e:
        abort(400, description=e.message)
    return {'result': True, 'data': data}
