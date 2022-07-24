# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from common_utilities.emails.email_confirmation import send_email_confirmation
from flask import request, jsonify, url_for
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_login import login_user
from project import serial
from project.auth.json_schema_validation.login_validation import validate_login_schema
from project.auth.serializer.login_schema import LoginSchema
from werkzeug.security import check_password_hash

from . import auth_blueprint, send_email, fetch_single_record


# <==================================================================================================>
#                                             LOGIN
# <==================================================================================================>
@auth_blueprint.route('/login', methods=['POST'])
def login():
    input_request = request.get_json()
    response = validate_login_schema(input_request)

    email = response["data"]["email"].lower()
    password = response["data"]["password"]

    user = fetch_single_record(email=email)

    if not user.email_confirmed:
        msg = "please confirm your email address"
        token = serial.dumps(email, salt='email_confirm')
        link = url_for('auth.email_confirmed', token=token, _external=True)
        send_email(target=send_email_confirmation, args=(user, link))
        return jsonify({"result": True, "msg": msg})

    if user and check_password_hash(user.password, password):
        login_user(user)
        user.is_logged_in = True
        user.save()
        print(f"Auth: login: logged in: {email}")

        ma_schema = LoginSchema()
        user_objs = ma_schema.dump(user)

        jwt_obj = {"email": email}
        access_token = create_access_token(identity=jwt_obj)
        refresh_token = create_refresh_token(identity=jwt_obj)

        return_obj = {
            "user": user_objs,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return {
            "result": True,
            "data": return_obj
        }
    else:

        return jsonify({"result": False, "msg": "wrong credentials"})
