# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from . import auth_blueprint, check_if_user_is_logged_in, return_data


# <==================================================================================================>
#                                       IMPORT ROUTES
# <==================================================================================================>
@auth_blueprint.route("/refresh-jwt-token", methods=["POST"])
@jwt_required(refresh=True)
@check_if_user_is_logged_in()
def refresh():
    email = get_jwt_identity()
    identity = {"email": email}
    access_token = create_access_token(identity=identity, fresh=False)
    data = {
        "token": access_token
    }

    return return_data(True, "success", data)
