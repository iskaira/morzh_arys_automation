from contextlib import suppress
from typing import Union, List, Any, Optional

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types.base import Boolean
from aiogram.utils.exceptions import (
    BadRequest, TelegramAPIError,
    Unauthorized, ChatNotFound,
)
from loguru import logger

from app.models.message import Message as DBMessage, BotMessage
from app.models.user import User, Status


async def safe_delete(message: Message):
    with suppress(TelegramAPIError):
        await message.delete()


async def delete_message_by_id(chat_id: int, message_id: int):
    with suppress(TelegramAPIError):
        from app.misc import bot
        await bot.delete_message(chat_id, message_id)


async def safe_answer_callback(clb: CallbackQuery, text=None, show_alert=None,
                               cache_time=None, url=None):
    try:
        await clb.answer(text=text, show_alert=show_alert, cache_time=cache_time,
                         url=url)
    except Exception as e:
        logger.warning(e)


async def smart_send_message(chat_id, splitted_text: list, parse_mode,
                             reply_markup=None,
                             disable_web_page_preview=True):
    messages = []
    splitted_size = len(splitted_text)
    from app.misc import bot
    for i in range(splitted_size):
        text = splitted_text[i]
        tmp_markup = None
        if i == splitted_size - 1:
            tmp_markup = reply_markup
        message = await bot.send_message(
            chat_id, text, parse_mode=parse_mode,
            reply_markup=tmp_markup,
            disable_web_page_preview=disable_web_page_preview)
        messages.append(message)
    return messages


async def smart_edit_message(chat_id, splitted_text: list, parse_mode,
                             reply_markup=None,
                             message=None,
                             disable_web_page_preview=True):
    messages = []
    _size = len(splitted_text)
    from app.misc import bot
    for i in range(_size):
        text = splitted_text[i]
        tmp_markup = None
        if i == _size - 1:
            tmp_markup = reply_markup
        if i == 0:
            message = await message.edit_text(text, parse_mode=parse_mode,
                                              reply_markup=tmp_markup,
                                              disable_web_page_preview=True)
        if i > 0:
            message = await bot.send_message(
                chat_id, text, parse_mode=parse_mode,
                reply_markup=tmp_markup,
                disable_web_page_preview=disable_web_page_preview)
        messages.append(message)
    return messages


async def smart_send_file(file,
                          text: Union[str, None] = "",
                          chat_id: Union[int, None] = None,
                          reply_markup=None,
                          parse_mode="HTML",
                          state: FSMContext = None,
                          disable_web_page_preview=True):
    try:
        if not state and not chat_id:
            return "Can't send, user not found"
        if state:
            chat_id = state.chat
        messages = []
        message = None
        splitted_text = []
        if len(text) > 1024:
            splitted_text.append(text[:1024])
            from app.utils.helper import smart_split
            splitted_text = splitted_text + smart_split(text[1024:])
        else:
            splitted_text = [text]
        splitted_size = len(splitted_text)
        from app.misc import bot
        for i in range(splitted_size):
            text = splitted_text[i]
            tmp_markup = None
            if i == splitted_size - 1:
                tmp_markup = reply_markup
            if i == 0:
                with open(file, "rb") as file:
                    message = await bot.send_document(
                        chat_id,
                        document=file,
                        caption=text,
                        reply_markup=tmp_markup
                    )
            if i > 0:
                message = await bot.send_message(
                    chat_id, text, parse_mode=parse_mode,
                    reply_markup=tmp_markup,
                    disable_web_page_preview=disable_web_page_preview)
            messages.append(message)
        return messages
    except Exception as e:
        logger.error(f"{chat_id}\nERROR: \n{e}")


async def delete_message_by_data_id(key: str, state: FSMContext):
    async with state.proxy() as data:
        if data.get(key):
            await delete_message_by_id(state.chat, data[key])


async def delete_all_messages(state: FSMContext):
    await delete_message_by_data_id("first_message_id", state)
    await delete_message_by_data_id("second_message_id", state)
    await delete_message_by_data_id("form_message", state)
    old_messages = await DBMessage.filter(chat_id=state.chat)
    for message in old_messages:
        if not message.is_start:
            await delete_message_by_id(state.chat, message.message_id)
            await message.delete()


# TODO: REFACTOR CODE - URGENT
async def try_message(
        text: str = None,
        message: Union[types.Message, int, None] = None,
        chat_id: Union[int, None] = None,
        reply_markup: Union[
            types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove
        ] = None,
        return_body: bool = False,
        just_markup: bool = False,
        send_this: bool = True,
        parse_mode="HTML",
        state_id=None,
        state: FSMContext = None,
        save_message_db: bool = True
) -> Union[Union[None, int, Message, List[Any], List[Optional[Any]],
                 List[Union[Union[Message, Boolean], Any]]], Any]:
    from app.misc import bot
    if state:
        chat_id = state.chat
    if not text:
        return
    from app.utils.helper import smart_split
    splitted_text = smart_split(text)
    messages = []
    try:
        if message is None:
            if just_markup:
                raise ValueError("Cant send message with only markup")

            messages = await smart_send_message(chat_id, splitted_text,
                                                parse_mode=parse_mode,
                                                reply_markup=reply_markup)
        else:
            try:
                if isinstance(message, types.Message):
                    if message.from_user.id != bot.id:
                        raise BadRequest("Message is not from bot")
                if just_markup:
                    if isinstance(message, types.Message):
                        messages.append(await message.edit_reply_markup(reply_markup))
                    elif isinstance(message, int):
                        messages.append(await bot.edit_message_reply_markup(
                            chat_id, message,
                            reply_markup=reply_markup))
                    else:
                        raise TypeError("Bad type of argument 'message'")
                else:
                    if isinstance(message, types.Message):
                        messages = await smart_edit_message(chat_id=chat_id,
                                                            splitted_text=splitted_text,
                                                            message=message,
                                                            parse_mode=parse_mode,
                                                            reply_markup=reply_markup)
                    elif isinstance(message, int):
                        messages = await smart_edit_message(chat_id=chat_id,
                                                            splitted_text=splitted_text,
                                                            message=message,
                                                            parse_mode=parse_mode,
                                                            reply_markup=reply_markup)

                    else:
                        raise TypeError("Bad type of argument 'message'")
            except BadRequest as e:
                if e.match != 'message is not modified':
                    if state:
                        if state_id == 'first_message_id':
                            pass
                        else:
                            pass
                    if just_markup:
                        raise ValueError("Cant send message with only markup")
                    if send_this:
                        if isinstance(message, types.Message):
                            messages = await smart_send_message(
                                chat_id, splitted_text,
                                parse_mode=parse_mode,
                                reply_markup=reply_markup)

                        elif isinstance(message, int):
                            messages = await smart_send_message(
                                chat_id, splitted_text,
                                parse_mode=parse_mode,
                                reply_markup=reply_markup)
                        else:
                            raise TypeError("Bad type of argument 'message'")
                else:
                    return message
    except Unauthorized as e:
        logger.warning(f"{chat_id} {str(e)} ")
        reason_user = False
        if e.check("Forbidden: bot was blocked by the user"):
            user = await User.filter(id=chat_id).first()
            if user:
                await user.update(status=Status.BLOCKED.value)
                reason_user = True
        if e.check("Forbidden: user is deactivated"):
            user = await User.filter(id=chat_id).first()
            if user:
                user.status = Status.DEACTIVATED.value
                await user.save(update_fields=['status'])
                reason_user = True
        if reason_user:

            if not return_body:
                return -1
            return messages
    except ChatNotFound as e:
        logger.warning(f"{chat_id} {str(e)} ")
        reason_user = False
        if e.check("ChatNotFound: Chat not found"):
            user = await User.filter(id=chat_id).first()
            if user:
                user.status = Status.CHAT_NOT_FOUND.value
                await user.save(update_fields=['status'])
                reason_user = True
        if reason_user:
            if not return_body:
                return -1
            return messages
    if not messages:
        logger.error(f"{chat_id}: No messages []")
        return
    json_reply_markup = None
    if reply_markup:
        json_reply_markup = reply_markup.as_json()
    if save_message_db:
        for message in messages:
            await BotMessage.create(
                text=message.text,
                chat_id=chat_id,
                message_id=message.message_id,
                reply_keyboard_json=json_reply_markup
            )
    if return_body:
        return messages[-1]
    return messages[-1].message_id
