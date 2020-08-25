import os

from pyrogram import (
    Client,
    filters
)
from pyrogram.types import Message
from bot import (
    AUTHORIZED_CHATS,
    OWNER_ID,
    download_dict,
    download_dict_lock,
    DOWNLOAD_DIR
)
from bot.helper.ext_utils.fs_utils import clean_download
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *

from time import sleep
from bot.helper.ext_utils.bot_utils import getDownloadByGid, MirrorStatus


@Client.on_message(
    filters.command(BotCommands.CancelMirror) &
    filters.chat(AUTHORIZED_CHATS)
)
def cancel_mirror(client: Client, message: Message):
    args = message.text.split(" ", maxsplit=1)
    mirror_message = None
    if len(args) > 1:
        gid = args[1]
        dl = getDownloadByGid(gid)
        if not dl:
            sendMessage(
                f"GID: <code>{gid}</code> not found.",
                client,
                message
            )
            return
        with download_dict_lock:
            keys = list(download_dict.keys())
        mirror_message = dl.message
    elif message.reply_to_message:
        mirror_message = message.reply_to_message
        with download_dict_lock:
            keys = list(download_dict.keys())
            dl = download_dict[mirror_message.message_id]
    if len(args) == 1:
        if mirror_message is None or mirror_message.message_id not in keys:
            if BotCommands.MirrorCommand in mirror_message.text or \
                    BotCommands.TarMirrorCommand in mirror_message.text:
                msg = "Mirror already have been cancelled"
                sendMessage(msg, client, message)
                return
            else:
                msg = "Please reply to the /mirror message which was used to start the download or /cancel gid to cancel it!"
                sendMessage(msg, client, message)
                return
    if dl.status() == "Uploading":
        sendMessage("Upload in Progress, Don't Cancel it.", client, message)
        return
    elif dl.status() == "Archiving":
        sendMessage("Archival in Progress, Don't Cancel it.", client, message)
        return
    else:
        dl.download().cancel_download()
    sleep(1)  # Wait a Second For Aria2 To free Resources.
    clean_download(
        os.path.join(
            DOWNLOAD_DIR,
            str(mirror_message.message_id)
        ) + os.path.sep
    )


@Client.on_message(
    filters.command(BotCommands.CancelAllCommand) &
    filters.user(OWNER_ID)
)
def cancel_all(client: Client, message: Message):
    with download_dict_lock:
        count = 0
        for dlDetails in list(download_dict.values()):
            if dlDetails.status() == MirrorStatus.STATUS_DOWNLOADING \
                    or dlDetails.status() == MirrorStatus.STATUS_WAITING:
                dlDetails.download().cancel_download()
                count += 1
    delete_all_messages()
    sendMessage(f'Cancelled {count} downloads!', client, message)
