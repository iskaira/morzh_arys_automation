from tortoise import fields

from app.models.base import AbstractBaseModel, TimestampedMixin


# TODO: refactor ForeignKeyRelation
# noinspection PyUnresolvedReferences
class UserAction(AbstractBaseModel, TimestampedMixin):
    message_text = fields.TextField(null=True)
    callback_data = fields.CharField(max_length=256, null=True)
    message_type = fields.CharField(max_length=128, null=True)
    current_state = fields.CharField(max_length=256, null=True)
    full_update_json = fields.TextField(null=True)
    state_data = fields.JSONField(null=True, default={})
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        'models.User',
        to_field='id'
    )
