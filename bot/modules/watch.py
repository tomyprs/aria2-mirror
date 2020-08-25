import os
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import Message
from bot import AUTHORIZED_CHATS, Interval, DOWNLOAD_DIR, DOWNLOAD_STATUS_UPDATE_INTERVAL, LOGGER
from bot.helper.ext_utils.bot_utils import setInterval
from bot.helper.telegram_helper.message_utils import update_all_messages, sendMessage, sendStatusMessage
from .mirror import MirrorListener
from bot.helper.mirror_utils.download_utils.youtube_dl_download_helper import YoutubeDLHelper
from bot.helper.telegram_helper.bot_commands import BotCommands
import threading


def _watch(bot: Client, update: Message, args: list, isTar=False):
    try:
        link = args[0]
    except IndexError:
        sendMessage(f'/{BotCommands.WatchCommand} [yt_dl supported link] to mirror with youtube_dl', bot, update)
        return
    reply_to = update.reply_to_message
    if reply_to is not None:
        tag = reply_to.from_user.username
    else:
        tag = None

    listener = MirrorListener(bot, update, isTar, tag)
    ydl = YoutubeDLHelper(listener)
    threading.Thread(
        target=ydl.add_download,args=(
            link,
            os.path.join(
                DOWNLOAD_DIR,
                str(listener.uid)
            )
        )
    ).start()
    sendStatusMessage(update, bot)
    if len(Interval) == 0:
        Interval.append(setInterval(DOWNLOAD_STATUS_UPDATE_INTERVAL, update_all_messages))


@Client.on_message(
    filters.command(BotCommands.WatchCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def watch(client: Client, message: Message):
    args = [" ".join(message.command[1:])]
    _watch(client, message, args)


@Client.on_message(
    filters.command(BotCommands.TarWatchCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def watchTar(client: Client, message: Message):
    args = [" ".join(message.command[1:])]
    _watch(client, message, args, True)
