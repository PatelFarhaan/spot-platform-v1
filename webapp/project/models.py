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
    password_reset_meta_data = db.DictField()
    last_name = db.StringField(max_length=70)
    first_name = db.StringField(max_length=70)
    password_confirm_meta_data = db.DictField()
    is_logged_in = db.BooleanField(defalut=False)
    email = db.EmailField(required=True, unique=True)
    created = db.DateTimeField(default=datetime.datetime.now)

    meta = dict(indexes=['email', '-created', 'is_logged_in'])

    # def get_id(self):
    #     return {
    #         "user_id": str(self.id),
    #         "role": "users"}
