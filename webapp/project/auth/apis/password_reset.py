# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import request
from project.auth.json_schema_validation.password_reset_validation import validate_password_reset_schema
from project.models import Users
from werkzeug.security import generate_password_hash

from . import auth_blueprint, return_data


# <==================================================================================================>
#                                      PASSWORD RESET LINK
# <==================================================================================================>
@auth_blueprint.route('/reset-password', methods=['POST'])
def reset_link():
    body = request.get_json()
    validate_password_reset_schema(body)

    email = body["email"].lower()
    secret_code = body["secret_code"]
    new_password = body["new_password"]
    confirm_password = body["confirm_password"]

    if new_password != confirm_password:
        print(f"Auth: reset-link: new and confirm password does not match: {email}")
        return return_data(False, "Both passwords should be same")

    user = Users.fetch_one_record(email=email)

    if generate_password_hash(new_password) == user.password:
        print(f"Auth: reset-link: old and new password cannot be the same: {email}")
        return return_data(False, "New and old password cannot be the same. Please choose a new password.")

    if secret_code != user.password_reset_code:
        print(f"Auth: reset-link: password reset secret code did not match: {email}")
        return return_data(False, "Invalid secret code.")

    user.hash_password()
    user.password_reset_code = ""
    user.save()
    print(f"Auth: reset-link: password changed: {email}")
    return return_data(True, "password successfully changed.")
