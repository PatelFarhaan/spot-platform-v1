# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from . import auth_blueprint, check_if_user_is_logged_in


# <==================================================================================================>
#                                       IMPORT ROUTES
# <==================================================================================================>
@auth_blueprint.route("/refresh-jwt-token", methods=["POST"])
@jwt_required(refresh=True)
@check_if_user_is_logged_in()
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify({
        "result": True,
        "token": access_token
    })
