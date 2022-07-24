# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from common_utilities.emails.forgot_password import send_forgot_password_email
from flask import request, jsonify
from project.auth.json_schema_validation.forgot_password_validation import validate_forgot_password_schema

from . import auth_blueprint, generate_password, send_email, fetch_single_record


# <==================================================================================================>
#                                       PASSWORD RESET REQUEST
# <==================================================================================================>
@auth_blueprint.route('/forgot-password', methods=['POST'])
def forgot_password_request():
    input_request = request.get_json()
    response = validate_forgot_password_schema(input_request)

    email = response["data"]["email"].lower()
    user = fetch_single_record(email=email)

    secret_code = generate_password(7)
    user.password_reset_code = secret_code
    user.save()
    print(f"Auth: forgot-password: forgot password code generated: {email}")
    send_email(target=send_forgot_password_email, args=(user, secret_code,))

    return jsonify({"result": True, "msg": "email sent if the user exists"})
