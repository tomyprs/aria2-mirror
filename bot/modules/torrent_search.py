import requests
import time

from bot import dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import editMessage, sendMessage
from telegram import update
from telegram.ext import run_async, CommandHandler


@run_async
def tor_search(update, context):
    message = update.message.text
    query = message.split(" ", maxsplit=1)[1]
    msg = sendMessage("Searching for available torrents...", context.bot, update)
    api_url = "https://api.sumanjay.cf/torrent/?query=" + query

    r = requests.get(api_url)
    try:
        torrents = r.json()
        reply_ = ""
        for torrent in torrents:
            if len(reply_) < 4096:
                try:
                    reply_ = (
                        reply_ + f"\n\n<b>{torrent['name']}</b>\n"
                        f"<b>Site : </b>{torrent['site']}\n"
                        f"<b>Size : </b>{torrent['size']}\n"
                        f"<b>Seeders : </b>{torrent['seeder']}\n"
                        f"<b>Leechers : </b>{torrent['leecher']}\n"
                        f"<code>{torrent['magnet']}</code>"
                    )
                    editMessage(reply_, msg)
                    time.sleep(0.5)
                except BaseException:
                    pass

        if reply_ == "":
            editMessage(f"No torrents found for {query}", msg)

    except BaseException:
        editMessage("Torrent Search API is down\nTry again later", msg)


tor_search_handler = CommandHandler(
    command=BotCommands.TorrentSearchCommand,
    callback=tor_search,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
)
dispatcher.add_handler(tor_search_handler)
