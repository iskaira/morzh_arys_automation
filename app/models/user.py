from enum import Enum

from aiogram.utils.mixins import ContextInstanceMixin
from tortoise import fields

from ..models.base import AbstractBaseModel, TimestampedMixin


class Status(Enum):
    BLOCKED = "BLOCKED"
    ACTIVE = "ACTIVE"
    DEACTIVATED = "DEACTIVATED"
    CHAT_NOT_FOUND = "CHAT_NOT_FOUND"


class AccessStatus(Enum):
    BANNED = "BANNED"
    WAITING = "WAITING"
    ACTIVE = "ACTIVE"


class User(ContextInstanceMixin, TimestampedMixin, AbstractBaseModel):
    id = fields.BigIntField(pk=True)

    firstname = fields.CharField(max_length=255, null=True)
    surname = fields.CharField(max_length=255, null=True)
    username = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    phone = fields.CharField(max_length=255, null=True)
    lang = fields.CharField(max_length=8, null=True)

    status = fields.CharField(default=Status.ACTIVE.value, max_length=32, index=True)

    class Meta:
        table = "users"
        table_description = (
            "This table contains information about all users who have "
            'ever sent "/start" to bot'
        )

    def __str__(self):
        return f"{self.id}:{self.firstname}"
