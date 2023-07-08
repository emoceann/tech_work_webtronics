from tortoise import Model, fields


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=256, unique=True)
    password = fields.CharField(max_length=256)
    email = fields.CharField(max_length=128, unique=True)
