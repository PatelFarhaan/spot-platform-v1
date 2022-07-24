# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import request
from flask_jwt_extended import jwt_required, current_user
from project.application.json_schema_validation.create_application_validation import validate_create_application_schema
from project.application.serializer.create_application_schema import CreateApplicationSchema
from project.models import Application

from . import application_blueprint, check_if_user_is_logged_in


# <==================================================================================================>
#                                        CREATE APPLICATION
# <==================================================================================================>
# TODO: will need to pull more information regarding the application from the Terraform file in S3 and store in the db


@application_blueprint.route('/dashbaord', methods=['POST'])
@jwt_required()
@check_if_user_is_logged_in()
def application():
    input_request = request.get_json()
    response = validate_create_application_schema(input_request)

    response["user"] = current_user
    new_application = Application(**response)
    new_application.save()

    ma_schema = CreateApplicationSchema()
    application_schema = ma_schema.dump(new_application)

    return_obj = {
        "application": application_schema,
    }

    return {
        "result": True,
        "data": return_obj

    }
