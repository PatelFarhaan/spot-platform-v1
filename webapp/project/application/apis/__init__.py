# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from functools import wraps

from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import current_user
from project import jwt
from project.models import Application, Users

# <==================================================================================================>
#                                    BLUEPRINT
# <==================================================================================================>
application_blueprint = Blueprint('application', __name__, url_prefix='/api/v1/application')


# <==================================================================================================>
#                                   DEFINING USER IDENTITY LOOKUP
# <==================================================================================================>
@jwt.user_identity_loader
def user_identity_lookup(user):
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
#                              FETCH SINGLE RECORD FROM THE DATABASE
# <==================================================================================================>
def fetch_single_record(**kwargs):
    app = Application.objects.filter(**kwargs).first()
    return app


# <==================================================================================================>
#                              FETCH MULTIPLE RECORD FROM THE DATABASE
# <==================================================================================================>
def fetch_multiple_record(**kwargs):
    apps = Application.objects.filter(**kwargs).all()
    return apps


# <==================================================================================================>
#                                       IMPORT ROUTES
# <==================================================================================================>
from . import (dashboard, create_application)
