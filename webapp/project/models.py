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
    environment_variables = db.DictField()
    domain = db.StringField(max_length=150)
    ebs_volume_size = db.IntField(default=8)
    iam_role = db.StringField(max_length=150)
    aws_region = db.StringField(max_length=70)
    ssh_key_name = db.StringField(max_length=70)
    aws_ecr_acc_id = db.StringField(max_length=150)
    platform = db.StringField(max_length=70, default="spotops")
    app_name = db.StringField(required=True, unique=True, max_length=100)
    environment = db.StringField(choices=('Development', 'Staging', 'Production'))

    meta = dict(indexes=['app_name', 'environment'])


# <==================================================================================================>
#                                       DATABASE COLLECTION
# <==================================================================================================>
class Database(db.Document, UserMixin):
    port = db.IntField()
    user = db.ReferenceField(Users)
    name = db.StringField(max_length=70)
    host = db.StringField(max_length=100)
    version = db.StringField(max_length=10)
    username = db.StringField(max_length=100)
    password = db.StringField(max_length=100)
    application = db.ReferenceField(Application)
    type = db.StringField(choices=('postgresql', 'mysql', 'mongodb'))

    meta = dict(indexes=['name'])


# <==================================================================================================>
#                                       AWS COLLECTION
# <==================================================================================================>
class Awscredentials(db.Document, UserMixin):
    user = db.ReferenceField(Users)
    company = db.StringField(max_length=70)
    access_key = db.StringField(max_length=250)
    secret_key = db.StringField(max_length=250)
    name = db.StringField(max_length=70, required=True, unique=True)

    meta = dict(indexes=['user'])
