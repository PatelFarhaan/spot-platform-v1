# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
import ipdb
from common_utilities.emails.email_confirmation import send_email_confirmation
from flask import url_for, request
from project import serial
from project.auth.json_schema_validation.register_validation import validate_register_schema
from project.models import Users

from . import auth_blueprint, send_email, return_data


# <==================================================================================================>
#                                          REGISTER
# <==================================================================================================>
@auth_blueprint.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    validate_register_schema(body)

    email = body["email"].lower()
    new_user = Users(**body)
    new_user.check_if_email_exists()
    new_user.hash_password()
    new_user.lower_email()
    new_user.save()
    print(f"Auth: register: created {email}")

    token = serial.dumps(email, salt='email_confirm')
    link = url_for('auth.email_confirmed', token=token, _external=True)
    send_email(target=send_email_confirmation, args=(new_user, link))

    return return_data(True, "user created")
