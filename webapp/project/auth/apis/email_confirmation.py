# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from flask import jsonify
from project import serial

from . import auth_blueprint, fetch_single_record


# <==================================================================================================>
#                                   EMAIL CONFIRMATION TOKEN
# <==================================================================================================>
@auth_blueprint.route('/email-confirmed/<token>', methods=['GET'])
def email_confirmed(token):
    try:
        email = serial.loads(token, salt='email_confirm').lower()
        print(f"Auth: email-confirmed: email confirmation link clicked: {email}")
    except Exception as e:
        print(f"Auth: email-confirmed: There was an error confirming the email: {e}")
        return jsonify(
            {"result": False, "msg": "There was an error while confirming the email address. Please try again."})

    user = fetch_single_record(email=email)

    if user.password_confirm_meta_data == {}:
        return jsonify(
            {"result": False, "msg": "This link has already been used."})

    print(f"Auth: email-confirmed: email confirmed: {email}")
    user.email_confirmed = True
    user.is_logged_in = False
    user.password_confirm_meta_data = {}
    user.save()
    print(f"Auth: email-confirmed: logged in: {email}")

    return jsonify(
        {"result": True, "msg": "Email is confirmed. Please login."})
