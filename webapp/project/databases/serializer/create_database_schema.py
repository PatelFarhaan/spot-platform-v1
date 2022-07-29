# <==================================================================================================>
#                                     IMPORTS
# <==================================================================================================>
from flask_marshmallow import fields as fd
from project import ma
from project.auth.serializer.login_schema import LoginSchema


# <==================================================================================================>
#                                     INVESTOR USER SCHEMA
# <==================================================================================================>
class CreateDatabaseSchema(ma.Schema):
    id = fd.fields.String()
    user = fd.fields.Method("get_users_schema")

    def get_users_schema(self, application_object):
        ma_schema = LoginSchema()
        return ma_schema.dump(application_object.user)

    class Meta:
        fields = (
            "tags", "od_config", "spot_config", "user", "security_groups", "ebs_volume_size", "app_name", "iam_role",
            "aws_region", "ssh_key_name", "aws_ecr_acc_id", "platform", "environment")
