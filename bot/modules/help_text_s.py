import pickle
import shutil, psutil
import time
from os import execl
from sys import executable
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import Message
from bot import (
    botStartTime,
    AUTHORIZED_CHATS,
    OWNER_ID
)
import bot.helper.ext_utils.fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from bot.helper.ext_utils.bot_utils import (
    get_readable_file_size,
    get_readable_time
)


@Client.on_message(
    filters.command(BotCommands.StatsCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def stats(client: Client, message: Message):
    currentTime = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    stats = f'Bot Uptime: {currentTime}\n' \
            f'Total disk space: {total}\n' \
            f'Used: {used}\n' \
            f'Free: {free}\n' \
            f'CPU: {cpuUsage}%\n' \
            f'RAM: {memory}%'
    sendMessage(stats, client, message)


@Client.on_message(
    filters.command(BotCommands.StartCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def start(client: Client, message: Message):
    start_string = f'''
This is a bot which can mirror all your links to Google drive!
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
    sendMessage(start_string, client, message)


@Client.on_message(
    filters.command(BotCommands.RestartCommand) &
    filters.user(OWNER_ID)
)
def restart(client: Client, message: Message):
    restart_message = sendMessage(
        "Restarting, Please wait!",
        client,
        message
    )
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@Client.on_message(
    filters.command(BotCommands.PingCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def ping(client: Client, message: Message):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", client, message)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@Client.on_message(
    filters.command(BotCommands.LogCommand) &
    filters.user(OWNER_ID)
)
def log(client: Client, message: Message):
    sendLogFile(client, message)


@Client.on_message(
    filters.command(BotCommands.HelpCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def bot_help(client: Client, message: Message):
    help_string = f'''
/{BotCommands.HelpCommand}: To get this message

/{BotCommands.MirrorCommand} [download_url][magnet_link]: Start mirroring the link to google drive

/{BotCommands.UnzipMirrorCommand} [download_url][magnet_link] : starts mirroring and if downloaded file is any archive , extracts it to google drive

/{BotCommands.TarMirrorCommand} [download_url][magnet_link]: start mirroring and upload the archived (.tar) version of the download

/{BotCommands.WatchCommand} [youtube-dl supported link]: Mirror through youtube-dl 

/{BotCommands.TarWatchCommand} [youtube-dl supported link]: Mirror through youtube-dl and tar before uploading

/{BotCommands.CancelMirror} : Reply to the message by which the download was initiated and that download will be cancelled

/{BotCommands.StatusCommand}: Shows a status of all the downloads

/{BotCommands.ListCommand} [search term]: Searches the search term in the Google drive, if found replies with the link

/{BotCommands.StatsCommand}: Show Stats of the machine the bot is hosted on

/{BotCommands.LogCommand}: Get a log file of the bot. Handy for getting crash reports

'''
    sendMessage(help_string, client, message)
