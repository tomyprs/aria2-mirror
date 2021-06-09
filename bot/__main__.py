import shutil, psutil
import signal
import pickle

from os import execl, path, remove
from sys import executable
import time

from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, delete, usage, torrent_search


@run_async
def stats(update, context):
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
    sendMessage(stats, context.bot, update)


@run_async
def start(update, context):
    LOGGER.info('UID: {} - UN: {} - MSG: {}'.format(update.message.chat.id,update.message.chat.username,update.message.text))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        if update.message.chat.type == "private" :
            sendMessage("This is a bot which can mirror all your links to Google drive!\nType /help to see all the commands", context.bot, update)
        else :
            sendMessage(f"Hey <b>{update.effective_user.first_name}</b>. This is a bot which can mirror all your links to Google drive!\nType /help to see all the commands", context.bot, update)
    else :
        sendMessage(f"Hey, <b>{update.message.chat.first_name}.</b> You're not authorized to use this bot.", context.bot, update)


@run_async
def restart(update, context):
    restart_message = sendMessage("Restarting, Please wait!", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)


@run_async
def bot_help(update, context):
    help_string_adm = f'''
/{BotCommands.MirrorCommand} [URL or Magnet]: Upload file to GDrive.

/{BotCommands.UnzipMirrorCommand} [URL or Magnet]: Unzip and Upload to GDrive.

/{BotCommands.TarMirrorCommand} [URL or Magnet]: Upload file as .tar.

/{BotCommands.WatchCommand} [YTDL Supported Link]: Upload video to GDdrive.

/{BotCommands.TarWatchCommand} [YTDL Supported Link]: Upload video as .tar.

/{BotCommands.CloneCommand} [GD Public Link]: Clone file/folder from GD.

/{BotCommands.CancelMirror} [GID or Reply to Command]: Use it to cancel download.

/{BotCommands.StatusCommand} : Shows the downloads status.

/{BotCommands.StatsCommand} : Show server stats.

/{BotCommands.ListCommand} [Query]: Searches file/folder in GD.

/{BotCommands.TorrentSearchCommand} [Query] : For searching torrent.

/{BotCommands.CancelAllCommand} : Cancel all downloads (Owner and Sudo only).

/{BotCommands.deleteCommand} [GD Link]: Delete file/folder from GD (Owner and Sudo only).

/{BotCommands.UsageCommand} : To see Heroku Dyno Stats (Owner and Sudo only).

/{BotCommands.RestartCommand} : Restart Bot (Owner and Sudo only).

/{BotCommands.AuthorizeCommand} : Authorize user/group (Owner and Sudo only).

/{BotCommands.UnAuthorizeCommand} : Unauthorize user/group  (Owner and Sudo only).

/{BotCommands.AuthorizedUsersCommand} : See authorized users/groups (Owner and Sudo only).

/{BotCommands.AddSudoCommand} : Add Sudo user (Owner only).

/{BotCommands.RmSudoCommand} : Remove Sudo user (Owner only).

/{BotCommands.LogCommand} : Get log file (Owner and Sudo only).

'''

    help_string = f'''
/{BotCommands.MirrorCommand} [URL or Magnet]: Upload file to GDrive.

/{BotCommands.UnzipMirrorCommand} [URL or Magnet]: Unzip and Upload to GDrive.

/{BotCommands.TarMirrorCommand} [URL or Magnet]: Upload file as .tar.

/{BotCommands.WatchCommand} [YTDL Supported Link]: Upload video to GDdrive.

/{BotCommands.TarWatchCommand} [YTDL Supported Link]: Upload video as .tar.

/{BotCommands.CloneCommand} [GD Public Link]: Clone file/folder from GD.

/{BotCommands.CancelMirror} [GID or Reply to Command]: Use it to cancel download.

/{BotCommands.StatusCommand} : Shows the downloads status.

/{BotCommands.StatsCommand} : Show server stats.

/{BotCommands.ListCommand} [Query]: Searches file/folder in GD.

/{BotCommands.TorrentSearchCommand} [Query] : For searching torrent.

'''

    if CustomFilters.sudo_user(update) or CustomFilters.owner_filter(update):
        if update.message.chat.type == "private":
            sendMessage(help_string_adm, context.bot, update)
        else:
            sendMessage("Please contact me in PM and send <code>/help</code>", context.bot, update)
    else:
        if update.message.chat.type == "private":
            sendMessage(help_string, context.bot, update)
        else:
            sendMessage("Please contact me in PM and send <code>/help</code>", context.bot, update)


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        remove('restart.pickle')

    start_handler = CommandHandler(BotCommands.StartCommand, start)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    help_handler = CommandHandler(BotCommands.HelpCommand, bot_help)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling()
    LOGGER.info("Bot Started")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


main()
