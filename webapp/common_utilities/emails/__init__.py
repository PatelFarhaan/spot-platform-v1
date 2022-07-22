# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from botocore.exceptions import ClientError
from common_utilities.aws import get_boto3_client

from .html_templates.confirmation_email_template import get_email_template


# <==================================================================================================>
#                                   SEND EMAIL LOGIC
# <==================================================================================================>
def send_email_logic(SENDER, RECIPIENT, SUBJECT, BODY_HTML):
    CHARSET = "UTF-8"
    ses_client = get_boto3_client("ses")

    try:
        ses_client.send_email(
            Destination={
                'ToAddresses': RECIPIENT,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(f"CM: email-cofirmation: {RECIPIENT}: failed: {e}")
    else:
        print(f"CM: email-cofirmation: {RECIPIENT}: success")
