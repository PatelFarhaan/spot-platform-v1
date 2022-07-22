# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from project.auth.json_schema_validation.update_information_validation import validate_update_information_schema
from project.auth.serializer.login_schema import LoginSchema

from . import auth_blueprint, check_if_user_is_logged_in


# <==================================================================================================>
#                                      UPDATE INFORMATION
# <==================================================================================================>
@auth_blueprint.route('/update-info', methods=['PATCH'])
@jwt_required(fresh=True)
@check_if_user_is_logged_in()
def update_info():
    input_data = request.get_json()
    response = validate_update_information_schema(input_data)
    data = response["data"]

    for field, new_value in data.items():
        setattr(current_user, field, new_value)
    current_user.save()

    ma_schema = LoginSchema()
    user_objs = ma_schema.dump(current_user)

    return jsonify({
        "result": True,
        "data": user_objs
    })
