# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import request, abort
from flask_jwt_extended import jwt_required, current_user
from mongoengine.errors import ValidationError, NotUniqueError
from project.credentials.json_schema_validation.create_aws_credentials_schema import \
    validate_create_aws_credentials_schema
from project.models import Awscredentials

from . import credentials_blueprint, check_if_user_is_logged_in, return_data


# <==================================================================================================>
#                                        CREATE AWS KEYS
# <==================================================================================================>
# TODO: Try to connect to Aws and see if the keys are valid and get the list of access it has

@credentials_blueprint.route('/create-credentials/aws', methods=['POST'])
@jwt_required()
@check_if_user_is_logged_in()
def create_aws_credentials():
    body = request.get_json()
    validate_create_aws_credentials_schema(body)

    body["user"] = current_user
    body["company"] = current_user.company

    try:
        Awscredentials(**body).save()
    except ValidationError as e:
        return return_data(False, str(e.errors))
    except NotUniqueError as e:
        print(e)
        return return_data(False, "credential name should be unique")
    except Exception as e:
        print(e)
        abort(500, "Some thing unexpected happened.")

    return return_data(True, "success")
