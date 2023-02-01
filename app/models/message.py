from tortoise import fields

from app.models.base import AbstractBaseModel, TimestampedMixin


class Message(AbstractBaseModel):
    chat_id = fields.BigIntField()
    message_id = fields.IntField()
    is_start = fields.BooleanField(default=False)


class BotMessage(AbstractBaseModel, TimestampedMixin):
    text = fields.TextField()
    chat_id = fields.BigIntField()
    message_id = fields.IntField()
    reply_keyboard_json = fields.TextField(null=True)
