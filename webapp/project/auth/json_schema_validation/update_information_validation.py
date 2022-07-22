# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from jsonschema import validate
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError

# <==================================================================================================>
#                                     REGISTER SCHEMA VALIDATION
# <==================================================================================================>
update_information_schema = {
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
        }
    },
    "required": ["first_name", "last_name", "company", "position"],
    "additionalProperties": False
}


def validate_update_information_schema(data):
    try:
        validate(instance=data, schema=update_information_schema)
    except ValidationError as e:
        return {'result': False, 'error': e.message}
    except SchemaError as e:
        return {'result': False, 'error': e.message}
    return {'result': True, 'data': data}
