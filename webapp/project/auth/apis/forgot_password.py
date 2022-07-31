# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from common_utilities.emails.forgot_password import send_forgot_password_email
from flask import request
from project.auth.json_schema_validation.forgot_password_validation import validate_forgot_password_schema
from project.models import Users

from . import auth_blueprint, generate_password, send_email, return_data


# <==================================================================================================>
#                                       PASSWORD RESET REQUEST
# <==================================================================================================>
@auth_blueprint.route('/forgot-password', methods=['POST'])
def forgot_password_request():
    body = request.get_json()
    validate_forgot_password_schema(body)

    email = body["email"].lower()
    user = Users.fetch_one_record(email=email)

    secret_code = generate_password(7)
    user.password_reset_code = secret_code
    user.save()
    print(f"Auth: forgot-password: forgot password code generated: {email}")
    send_email(target=send_forgot_password_email, args=(user, secret_code,))

    return return_data(True, "email sent")
