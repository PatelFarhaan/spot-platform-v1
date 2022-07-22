# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import request, jsonify
from project.auth.apis import auth_blueprint
from project.auth.json_schema_validation.password_reset_validation import validate_password_reset_schema
from project.models import Users
from werkzeug.security import generate_password_hash


# <==================================================================================================>
#                                      PASSWORD RESET LINK
# <==================================================================================================>
@auth_blueprint.route('/reset-password', methods=['POST'])
def reset_link():
    input_request = request.get_json()
    response = validate_password_reset_schema(input_request)

    if not response["result"]:
        return jsonify(response)

    email = response["data"]["email"].lower()
    secret_code = response["data"]["secret_code"]
    new_password = response["data"]["new_password"]
    confirm_password = response["data"]["confirm_password"]

    if new_password != confirm_password:
        print(f"Auth: reset-link: new and confirm password does not match: {email}")
        return jsonify(
            {"result": False, "msg": "Both passwords should be same"})

    user = Users.objects.filter(email=email).first()

    if not user:
        print(f"Auth: reset-link: user does not exist: {email}")
        return jsonify(
            {"result": False, "msg": "There was an error. Please try again."})

    if generate_password_hash(new_password) == user.password:
        print(f"Auth: reset-link: old and new password cannot be the same: {email}")
        return jsonify(
            {"result": False, "msg": "New and old password cannot be the same. Please choose a new password."})

    if secret_code != user.password_reset_code:
        print(f"Auth: reset-link: password reset secret code did not match: {email}")
        return jsonify(
            {"result": False, "msg": "Invalid secret code."})

    user.password = generate_password_hash(new_password)
    user.password_reset_code = ""
    user.save()
    print(f"Auth: reset-link: password changed: {email}")
    return jsonify(
        {"result": True, "msg": "password successfully changed."})
