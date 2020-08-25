from pyrogram import (
    Client,
    filters
)
from pyrogram.types import Message
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, AUTHORIZED_CHATS
from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage
import threading
from bot.helper.telegram_helper.bot_commands import BotCommands


@Client.on_message(
    filters.command(BotCommands.ListCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def list_drive(client: Client, message: Message):
    search = message.text.split(' ', maxsplit=1)[1]
    LOGGER.info(f"Searching: {search}")
    gdrive = GoogleDriveHelper(None)
    msg = gdrive.drive_list(search)
    if msg:
        reply_message = sendMessage(msg, client, message)
    else:
        reply_message = sendMessage('No result found', client, message)

    threading.Thread(target=auto_delete_message, args=(client, message, reply_message)).start()
