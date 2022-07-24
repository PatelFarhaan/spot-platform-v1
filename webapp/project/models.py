# <==================================================================================================>
#                                       IMPORTS
# <==================================================================================================>
import datetime

from flask_login import UserMixin
from project import db, login_manager


# <==================================================================================================>
#                                       GET USERS ID FOR LOGIN
# <==================================================================================================>
@login_manager.user_loader
def user_load(user_id):
    return Users.objects.get(pk=user_id)


# <==================================================================================================>
#                                          USERS COLLECTION
# <==================================================================================================>
class Users(db.Document, UserMixin):
    password = db.StringField()
    applications = db.DictField()
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

    meta = dict(indexes=['email', 'is_logged_in', 'applications'])


# <==================================================================================================>
#                                       APPLICATION COLLECTION
# <==================================================================================================>
class Application(db.Document, UserMixin):
    tags = db.DictField()
    od_config = db.DictField()
    spot_config = db.DictField()
    user = db.ReferenceField(Users)
    security_groups = db.DictField()
    ebs_volume_size = db.IntField(default=8)
    app_name = db.StringField(max_length=100)
    iam_role = db.StringField(max_length=150)
    aws_region = db.StringField(max_length=70)
    ssh_key_name = db.StringField(max_length=70)
    aws_ecr_acc_id = db.StringField(max_length=150)
    platform = db.StringField(max_length=70, default="spotops")
    environment = db.ListField(choices=('Development', 'Staging', 'Production'))

    meta = dict(indexes=['app_name', 'environment'])
