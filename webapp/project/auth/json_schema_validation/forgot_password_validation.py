# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from jsonschema import validate
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError

# <==================================================================================================>
#                                        LOGIN SCHEMA VALIDATION
# <==================================================================================================>
forgot_password_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        }
    },
    "required": ["email"],
    "additionalProperties": False
}


def validate_forgot_password_schema(data):
    try:
        validate(instance=data, schema=forgot_password_schema)
    except ValidationError as e:
        return {'result': False, 'error': e.message}
    except SchemaError as e:
        return {'result': False, 'error': e.message}
    return {'result': True, 'data': data}
