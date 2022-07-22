# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import request, jsonify, url_for, abort
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_login import login_user
from project import serial
from project.auth.apis import auth_blueprint, send_email
from project.auth.json_schema_validation.login_validation import validate_login_schema
from project.auth.serializer.login_schema import LoginSchema
from project.models import Users
from werkzeug.security import check_password_hash


# <==================================================================================================>
#                                             LOGIN
# <==================================================================================================>
@auth_blueprint.route('/login', methods=['POST'])
def login():
    input_request = request.get_json()
    response = validate_login_schema(input_request)

    email = response["data"]["email"].lower()
    password = response["data"]["password"]

    user = Users.objects.filter(email=email).first()

    if user is None:
        print(f"Auth: login: does not exist: {email}")
        abort(404, description="user does not exist")

    if not user.email_confirmed:
        msg = "please confirm your email address"
        token = serial.dumps(email, salt='email_confirm')
        link = url_for('auth.email_confirmed', token=token, _external=True)

        # todo: create email confirmation function
        # send_email(target=email_confirmation, args=(user, link, user.first_name))
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
        return {
            "result": True,
            "user": user_objs,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    else:
        return jsonify({"result": False, "msg": "wrong credentials"})
