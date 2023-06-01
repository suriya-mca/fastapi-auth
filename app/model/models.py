from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class UserInfo(models.Model):
	id = fields.UUIDField(pk=True)
	name = fields.CharField(max_length=50, null=False)
	email = fields.CharField(max_length=100, null=False)
	password = fields.CharField(max_length=100, null=False)


UserInfo_Pydantic = pydantic_model_creator(UserInfo, name="UserInfo")
UserInfoIn_Pydantic = pydantic_model_creator(UserInfo, name="UserInfoIn", exclude_readonly=True)