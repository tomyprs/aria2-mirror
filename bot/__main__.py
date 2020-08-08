import signal
import pickle
from os import path, remove
from pyrogram import Client
from bot import (
    BOT_TOKEN,
    DOWNLOAD_DIR,
    LOGGER,
    TELEGRAM_API,
    TELEGRAM_HASH
)
from bot.helper.ext_utils import fs_utils


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        remove('restart.pickle')

    plugins = dict(
        root="bot/modules"
    )
    app = Client(
        ":memory:",
        api_id=TELEGRAM_API,
        api_hash=TELEGRAM_HASH,
        plugins=plugins,
        bot_token=BOT_TOKEN,
        workdir=DOWNLOAD_DIR
    )

    app.set_parse_mode("html")

    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)

    app.run()


if __name__ == "__main__":
    main()
