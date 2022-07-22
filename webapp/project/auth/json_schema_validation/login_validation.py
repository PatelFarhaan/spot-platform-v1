# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
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
        return {'result': False, 'error': e.message}
    except SchemaError as e:
        return {'result': False, 'error': e.message}
    return {'result': True, 'data': data}
