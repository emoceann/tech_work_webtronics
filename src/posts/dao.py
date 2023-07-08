from tortoise import Model, fields


class Post(Model):
    id = fields.BigIntField(pk=True)
    creator = fields.ForeignKeyField("models.User", to_field="username", on_delete=fields.CASCADE)
    text = fields.CharField(max_length=2048)


class Reaction(Model):
    id = fields.BigIntField(pk=True)
    reaction_type = fields.CharField(max_length=10)
    user = fields.ForeignKeyField("models.User", to_field="username", on_delete=fields.SET_NULL, null=True)
    post = fields.ForeignKeyField("models.Post", on_delete=fields.CASCADE)
