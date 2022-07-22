# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
import datetime

from flask_login import UserMixin
from project import db, login_manager


# <==================================================================================================>
#                                       UPDATE INFORMATION
# <==================================================================================================>
@login_manager.user_loader
def user_load(user_id):
    return Users.objects.get(pk=user_id)


# <==================================================================================================>
#                                    INVESTOR COLLECTION
# <==================================================================================================>
class Users(db.Document, UserMixin):
    password = db.StringField()
    company = db.StringField(max_length=70)
    position = db.StringField(max_length=70)
    last_name = db.StringField(max_length=70)
    first_name = db.StringField(max_length=70)
    is_logged_in = db.BooleanField(defalut=False)
    email_confirmed = db.BooleanField(defalut=False)
    email = db.EmailField(required=True, unique=True)
    password_reset_code = db.StringField(max_length=70)
    created = db.DateTimeField(default=datetime.datetime.now)
    password_confirm_meta_data = db.DictField(default={"is_clicked": False})

    meta = dict(indexes=['email', 'is_logged_in'])
