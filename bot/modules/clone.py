from pyrogram import (
    Client,
    filters
)
from pyrogram.types import Message
from bot import (
    AUTHORIZED_CHATS
)
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import new_thread


@new_thread
@Client.on_message(
    filters.command(BotCommands.CloneCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def cloneNode(client: Client, message: Message):
    args = message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        link = args[1]
        msg = sendMessage(f"Cloning: <code>{link}</code>", client, message)
        gd = GoogleDriveHelper()
        result = gd.clone(link)
        deleteMessage(msg)
        sendMessage(result, client, message)
    else:
        sendMessage("Provide G-Drive Shareable Link to Clone.", client, message)
