# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
import random
import string
import threading
from functools import wraps

from flask import Blueprint, abort
from flask import jsonify
from flask_jwt_extended import current_user
from project import jwt
from project.models import Users

# <==================================================================================================>
#                                    BLUEPRINT
# <==================================================================================================>
auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


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
#                                        SEND EMAIL FUNCTION
# <==================================================================================================>
def send_email(**kwargs):
    thread = threading.Thread(**kwargs)
    thread.start()


# <==================================================================================================>
#                                        RANDOM PASSWORD GENERATOR
# <==================================================================================================>
def generate_password(password_length: int):
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    password = []

    for _ in range(password_length):
        password.append(random.choice(characters))

    random.shuffle(password)
    return "".join(password)


# <==================================================================================================>
#                              FETCH SINGLE RECORD FROM THE DATABASE
# <==================================================================================================>
def fetch_single_record(**kwargs):
    user = Users.objects.filter(**kwargs).first()

    if user is None:
        print(f"Auth: login: does not exist: {kwargs}")
        abort(404, description="user does not exist")

    return user


# <==================================================================================================>
#                                       IMPORT ROUTES
# <==================================================================================================>
from . import (register, login, logout, jwt_expired_check, forgot_password, update_information,
               email_confirmation, password_reset, refresh_jwt_token)
