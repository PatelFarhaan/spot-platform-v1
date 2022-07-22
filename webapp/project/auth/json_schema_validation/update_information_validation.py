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
        abort(400, description=e.message)
    except SchemaError as e:
        abort(400, description=e.message)
    return {'result': True, 'data': data}
