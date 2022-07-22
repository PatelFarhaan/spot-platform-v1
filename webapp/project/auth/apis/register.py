# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import url_for, request, jsonify
from project import serial
from project.auth.apis import auth_blueprint, send_email
from project.auth.json_schema_validation.register_validation import validate_register_schema
from project.models import Users
from werkzeug.security import generate_password_hash


# <==================================================================================================>
#                                          REGISTER
# <==================================================================================================>
@auth_blueprint.route('/register', methods=['POST'])
def register():
    input_request = request.get_json()
    response = validate_register_schema(input_request)

    email = response["data"]["email"].lower()
    email_exist = Users.objects.filter(email=email).first()

    if email_exist:
        print(f"Auth: register: exists: {email}")
        return jsonify({"result": False, "msg": "email exists"})

    input_request["password"] = generate_password_hash(input_request["password"])
    input_request["email"] = input_request["email"].lower()
    new_user = Users(**input_request)
    new_user.save()
    print(f"Auth: register: created {email}")

    token = serial.dumps(email, salt='email_confirm')
    link = url_for('auth.email_confirmed', token=token, _external=True)

    # todo: create a function for this:
    # send_email(target=email_confirmation, args=(new_user, link, input_request.get("first_name")))

    return jsonify({"result": True, "msg": "user created"})
