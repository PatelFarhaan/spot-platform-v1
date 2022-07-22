# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import jsonify
from flask_jwt_extended import jwt_required

from . import auth_blueprint, check_if_user_is_logged_in


# <==================================================================================================>
#                                  IS JWT TOKEN EXPIRED CHECK
# <==================================================================================================>
@auth_blueprint.route('/jwt-token-check', methods=["GET"])
@jwt_required()
@check_if_user_is_logged_in()
def expired_jwt_token_check():
    resp_obj = {
        "result": True,
        "msg": "token is valid"
    }
    return jsonify(resp_obj)
