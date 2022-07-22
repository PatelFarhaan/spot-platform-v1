# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from . import auth_blueprint


# <==================================================================================================>
#                                          LOGOUT
# <==================================================================================================>
@auth_blueprint.route('/logout', methods=["POST"])
@jwt_required()
def logout():
    current_user.is_logged_in = False
    current_user.save()
    print(f"users: logout: user logged out: {current_user.email}")
    return jsonify({"result": True, "msg": "user logged out"})
