from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery
from loguru import logger

from app.models.message import Message
from app.models.stat_user_action import UserAction
from app.models.user import Status


class DBMessageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def on_pre_process_my_chat_member(self, message: types.ChatMemberUpdated,
                                            _: dict):
        if message.chat.type == "private":
            try:
                from app.models.user import User
                user = await User.filter(id=message.chat.id).first()
                if message.new_chat_member.status == "kicked":
                    user.status = Status.BLOCKED.value
                    await user.save(update_fields=["status"])
            except Exception as e:
                logger.error(f"User: {message} \n\nError: {e}")

    async def on_process_callback_query(self, callback_query: CallbackQuery, _: dict):
        try:
            await callback_query.answer()
            if callback_query.message.chat.type == "private":
                from app.misc import storage
                state = FSMContext(storage, callback_query.from_user.id,
                                   callback_query.from_user.id)
                await UserAction.create(
                    user_id=callback_query.from_user.id,
                    callback_data=callback_query.data,
                    current_state=await state.get_state(),
                    state_data=await state.get_data(),
                    full_update_json=callback_query.as_json()
                )
        except Exception as e:
            logger.error(f"{callback_query} \n {e}")

    async def on_process_message(self, message: types.Message, _: dict):
        try:
            from app.misc import storage, bot
            from app import config
            state = FSMContext(storage, message.chat.id, message.chat.id)
            if message.chat.type == "private":
                await UserAction.create(
                    user_id=message.chat.id,
                    message_type=str(message.content_type),
                    message_text=message.text,
                    current_state=await state.get_state(),
                    state_data=await state.get_data(),
                    full_update_json=message.as_json()
                )

                from app.keyboards.utils.try_message import delete_message_by_id
                is_start = bool(await CommandStart().check(message))

                await Message.update_or_create(
                    message_id=message.message_id,
                    chat_id=message.chat.id,
                    is_start=is_start
                )
        except Exception as e:
            from app.keyboards.utils.try_message import try_message
            logger.error(f"{message} \n\n {e}")
