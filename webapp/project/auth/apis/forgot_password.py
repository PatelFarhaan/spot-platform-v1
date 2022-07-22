# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from common_utilities.emails.forgot_password import send_forgot_password_email
from flask import request, jsonify, abort
from project.auth.json_schema_validation.forgot_password_validation import validate_forgot_password_schema
from project.models import Users

from . import auth_blueprint, generate_password, send_email


# <==================================================================================================>
#                                       PASSWORD RESET REQUEST
# <==================================================================================================>
@auth_blueprint.route('/forgot-password', methods=['POST'])
def forgot_password_request():
    input_request = request.get_json()
    response = validate_forgot_password_schema(input_request)

    email = response["data"]["email"].lower()
    user = Users.objects.filter(email=email).first()

    if user is None:
        print(f"Auth: forgot-password: user does not exist : {email}")
        abort(404, description="email sent if the user exists")

    secret_code = generate_password(7)
    user.password_reset_code = secret_code
    user.save()
    print(f"Auth: forgot-password: forgot password code generated: {email}")
    send_email(target=send_forgot_password_email, args=(user, secret_code,))

    return jsonify({"result": True, "msg": "email sent if the user exists"})
