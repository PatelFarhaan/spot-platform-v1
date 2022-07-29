# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import request, abort
from flask_jwt_extended import jwt_required, current_user
from mongoengine.errors import ValidationError, NotUniqueError
from project.cloud_credentials.json_schema_validation.create_credentials_schema import \
    validate_create_credentials_schema
from project.models import Awscredentials

from . import cloud_credentials_blueprint, check_if_user_is_logged_in, return_data


# <==================================================================================================>
#                                        CREATE AWS KEYS
# <==================================================================================================>
# TODO: Try to connect to Aws and see if the keys are valid and get the list of access it has

@cloud_credentials_blueprint.route('/create-application', methods=['POST'])
@jwt_required()
@check_if_user_is_logged_in()
def application():
    input_request = request.get_json()
    response = validate_create_credentials_schema(input_request)

    response["user"] = current_user
    response["company"] = current_user.company

    try:
        new_credentials = Awscredentials(**response)
        new_credentials.save()
    except ValidationError as e:
        return return_data(False, str(e.errors))
    except NotUniqueError as e:
        print(e)
        return return_data(False, "credential name should be unique")
    except Exception as e:
        print(e)
        abort(500, "Some thing unexpected happened.")

    return return_data(True, "success")
