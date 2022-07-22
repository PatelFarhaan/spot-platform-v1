# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from . import send_email_logic
from .html_templates.forgot_password_email_template import get_email_template


# <==================================================================================================>
#                                   EMAIL CONFIRMATION
# <==================================================================================================>
def send_forgot_password_email(user, secret_code):
    RECIPIENT = [user.email]
    SENDER = "changeme@makedynamic.com"
    SUBJECT = f"{user.first_name}, please confirm your email address"
    BODY_HTML = get_email_template().format(secret_code=secret_code)
    send_email_logic(SENDER, RECIPIENT, SUBJECT, BODY_HTML)
