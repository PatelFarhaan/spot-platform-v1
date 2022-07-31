# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import request
from flask_jwt_extended import jwt_required, current_user
from project.auth.json_schema_validation.update_information_validation import validate_update_information_schema
from project.auth.serializer.login_schema import LoginSchema

from . import auth_blueprint, check_if_user_is_logged_in, return_data


# <==================================================================================================>
#                                      UPDATE INFORMATION
# <==================================================================================================>
@auth_blueprint.route('/update-info', methods=['PUT'])
@jwt_required()
@check_if_user_is_logged_in()
def update_info():
    body = request.get_json()
    validate_update_information_schema(body)

    current_user.update(**body)
    current_user.save()
    current_user.reload()

    ma_schema = LoginSchema()
    user_data = ma_schema.dump(current_user)

    return return_data(True, "success", user_data)
