from pyrogram import (
    Client,
    Filters,
    Message
)
from bot import AUTHORIZED_CHATS, status_reply_dict, DOWNLOAD_STATUS_UPDATE_INTERVAL, status_reply_dict_lock
from bot.helper.telegram_helper.message_utils import *
from time import sleep
from bot.helper.ext_utils.bot_utils import get_readable_message
from bot.helper.telegram_helper.bot_commands import BotCommands
import threading


@Client.on_message(
    Filters.command(BotCommands.StatusCommand) &
    Filters.chat(AUTHORIZED_CHATS)
)
def mirror_status(client: Client, update: Message):
    message = get_readable_message()
    if len(message) == 0:
        message = "No active downloads"
        reply_message = sendMessage(message, client, update)
        threading.Thread(target=auto_delete_message, args=(client, update, reply_message)).start()
        return
    index = update.chat.id
    with status_reply_dict_lock:
        if index in status_reply_dict.keys():
            deleteMessage(status_reply_dict[index])
            del status_reply_dict[index]
    sendStatusMessage(update, client)
    deleteMessage(update)
