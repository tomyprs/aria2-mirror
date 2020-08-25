from pyrogram import Client
from pyrogram.types import Message
import time
from bot import AUTO_DELETE_MESSAGE_DURATION, LOGGER, \
    status_reply_dict, status_reply_dict_lock
from bot.helper.ext_utils.bot_utils import get_readable_message


def sendMessage(text: str, bot: Client, message: Message):
    try:
        return bot.send_message(chat_id=message.chat.id,
                            reply_to_message_id=message.message_id,
                            text=text)
    except Exception as e:
        LOGGER.error(str(e))


def editMessage(text: str, message: Message):
    try:
        message.edit_text(text)
    except Exception as e:
        LOGGER.error(str(e))


def deleteMessage(message: Message):
    try:
        message.delete()
    except Exception as e:
        LOGGER.error(str(e))


def sendLogFile(bot: Client, message: Message):
    f = 'log.txt'
    bot.send_document(
        document=f,
        reply_to_message_id=message.message_id,
        chat_id=message.chat.id
    )


def auto_delete_message(bot, cmd_message: Message, bot_message: Message):
    if AUTO_DELETE_MESSAGE_DURATION != -1:
        time.sleep(AUTO_DELETE_MESSAGE_DURATION)
        try:
            # Skip if None is passed meaning we don't want to delete bot or cmd message
            deleteMessage(cmd_message)
            deleteMessage(bot_message)
        except AttributeError:
            pass


def delete_all_messages():
    with status_reply_dict_lock:
        for message in list(status_reply_dict.values()):
            try:
                deleteMessage(message)
                del status_reply_dict[message.chat.id]
            except Exception as e:
                LOGGER.error(str(e))


def update_all_messages():
    msg = get_readable_message()
    with status_reply_dict_lock:
        for chat_id in list(status_reply_dict.keys()):
            if status_reply_dict[chat_id] and msg != status_reply_dict[chat_id].text:
                try:
                    editMessage(msg, status_reply_dict[chat_id])
                except Exception as e:
                    LOGGER.error(str(e))
                status_reply_dict[chat_id].text = msg


def sendStatusMessage(msg: Message, bot: Client):
    progress = get_readable_message()
    with status_reply_dict_lock:
        if msg.chat.id in list(status_reply_dict.keys()):
            try:
                message = status_reply_dict[msg.chat.id]
                deleteMessage(message)
                del status_reply_dict[msg.chat.id]
            except Exception as e:
                LOGGER.error(str(e))
                del status_reply_dict[msg.chat.id]
                pass
        message = sendMessage(progress, bot, msg)
        status_reply_dict[msg.chat.id] = message
