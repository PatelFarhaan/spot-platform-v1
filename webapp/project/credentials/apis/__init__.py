# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from functools import wraps

from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import current_user
from project import jwt
from project.models import Users

# <==================================================================================================>
#                                    BLUEPRINT
# <==================================================================================================>
credentials_blueprint = Blueprint('credentials', __name__, url_prefix='/api/v1/credentials')


# <==================================================================================================>
#                                   DEFINING USER IDENTITY LOOKUP
# <==================================================================================================>
@jwt.user_identity_loader
def user_identity_lookup(user):
    print(user)
    return user["email"]


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.objects.filter(email=identity).first_or_404()


# <==================================================================================================>
#                                   CHECK IF USER IS LOGGED OFF
# <==================================================================================================>
def check_if_user_is_logged_in():
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if not current_user.is_logged_in:
                return jsonify({"result": True, "message": "user logged out"}), 403

            ret = f(*args, **kwargs)
            return ret

        return decorator

    return wrapper


# <==================================================================================================>
#                                           RETURN DATA
# <==================================================================================================>
def return_data(result, message, data=None):
    return jsonify({
        "result": result,
        "msg": message,
        "data": data
    })


# <==================================================================================================>
#                                       IMPORT ROUTES
# <==================================================================================================>
from . import (create_aws_credentials, create_github_credentials)
