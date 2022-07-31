# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
from project import serial
from project.models import Users

from . import auth_blueprint, return_data


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
        msg = "There was an error while confirming the email address. Please try again."
        return return_data(False, msg)

    user = Users.fetch_single_record(email=email)

    if user.password_confirm_meta_data == {}:
        return return_data(False, "This link has already been used.")

    print(f"Auth: email-confirmed: email confirmed: {email}")
    user.password_confirm_meta_data = {}
    user.email_confirmed = True
    user.is_logged_in = False
    user.save()
    print(f"Auth: email-confirmed: logged in: {email}")

    return return_data(True, "Email is confirmed. Please login.")
