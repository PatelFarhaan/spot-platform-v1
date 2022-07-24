# <==================================================================================================>
#                                     IMPORTS
# <==================================================================================================>
from flask_marshmallow import fields as fd
from project import ma


# <==================================================================================================>
#                                     INVESTOR USER SCHEMA
# <==================================================================================================>
class CreateApplicationSchema(ma.Schema):
    id = fd.fields.String()

    class Meta:
        fields = (
            "tags", "od_config", "spot_config", "user", "security_groups", "ebs_volume_size", "app_name", "iam_role",
            "aws_region", "ssh_key_name", "aws_ecr_acc_id", "platform", "environment")
