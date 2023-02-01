import asyncio
from typing import Optional

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from tortoise.timezone import now

from ..models.user import Status, User


class ACLMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self._process_user(data, message.from_user)

    async def on_pre_process_callback_query(
        self,
        query: types.CallbackQuery,
        data: dict,
    ):
        await self._process_user(data, query.from_user)

    async def on_pre_process_my_chat_member(
        self,
        chat_member_updated: types.ChatMemberUpdated,
        data: dict,
    ):
        await self._process_user(data, chat_member_updated.from_user, make_active=False)

    async def _process_user(
        self,
        data: dict,
        user: types.User,
        make_active: bool = True,
    ):
        user_db: Optional[User] = await User.filter(id=user.id).first()

        if not user_db:
            user_db = await self._create_user(user)
        else:
            asyncio.create_task(
                self._update_user(user_db, user, make_active=make_active)
            )

        data["user"] = user_db
        User.set_current(user_db)

    @staticmethod
    async def _create_user(user: types.User):
        user_data = {
            "id": user.id,
            "name": user.full_name,
        }
        if user.username is not None:
            user_data["username"] = user.username

        return await User.create(**user_data)

    @staticmethod
    async def _update_user(
        user_db: User,
        user: types.User,
        make_active: bool = True,
    ):
        modified = []
        check_list = {
            "username": user.username,
            "name": user.full_name,
            "updated_at": now(),
        }
        if make_active:
            check_list["status"] = Status.ACTIVE.value

        for field, value in check_list.items():
            if getattr(user_db, field) != value:
                setattr(user_db, field, value)
                modified.append(field)

        await user_db.save(update_fields=modified)
