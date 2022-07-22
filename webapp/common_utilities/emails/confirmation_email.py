# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from .html_templates.confirmation_email_template import get_email_template
from . import send_email_logic


# <==================================================================================================>
#                                   EMAIL CONFIRMATION
# <==================================================================================================>
def email_confirmation(user, email_confirm_link):
    RECIPIENT = [user.email]
    SENDER = "changeme@makedynamic.com"
    SUBJECT = f"{user.first_name}, please confirm your email address"
    BODY_HTML = get_email_template().format(email_confirm_link=email_confirm_link, first_name=user.first_name)
    send_email_logic(SENDER, RECIPIENT, SUBJECT, BODY_HTML)
