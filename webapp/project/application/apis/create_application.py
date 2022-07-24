# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import request, abort
from flask_jwt_extended import jwt_required, current_user
from mongoengine.errors import ValidationError, NotUniqueError
from project.application.json_schema_validation.create_application_validation import validate_create_application_schema
from project.application.serializer.create_application_schema import CreateApplicationSchema
from project.models import Application

from . import application_blueprint, check_if_user_is_logged_in, return_data


# <==================================================================================================>
#                                        CREATE APPLICATION
# <==================================================================================================>
# TODO: will need to pull more information regarding the application from the Terraform file in S3 and store in the db


@application_blueprint.route('/create-application', methods=['POST'])
@jwt_required()
@check_if_user_is_logged_in()
def application():
    input_request = request.get_json()
    response = validate_create_application_schema(input_request)

    app_name = response["app_name"]
    response["user"] = current_user

    try:
        new_application = Application(**response)
        new_application.save()
    except ValidationError as e:
        return return_data(False, str(e.errors))
    except NotUniqueError as e:
        print(e)
        return return_data(False, "app name should be unique")
    except Exception as e:
        print(e)
        abort(500, "Some thing unexpected happened.")

    if app_name not in current_user.applications:
        current_user.applications[app_name] = new_application.id
        current_user.save()

    ma_schema = CreateApplicationSchema()
    application_schema = ma_schema.dump(new_application)

    data = {
        "application": application_schema,
    }

    return return_data(True, "success", data)
