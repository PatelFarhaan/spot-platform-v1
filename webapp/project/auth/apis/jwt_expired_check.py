# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask_jwt_extended import jwt_required

from . import auth_blueprint, check_if_user_is_logged_in, return_data


# <==================================================================================================>
#                                  IS JWT TOKEN EXPIRED CHECK
# <==================================================================================================>
@auth_blueprint.route('/jwt-token-check', methods=["GET"])
@jwt_required()
@check_if_user_is_logged_in()
def expired_jwt_token_check():
    return return_data(True, "token is valid")
