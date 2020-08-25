#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://github.com/SpEcHiDe/TerminalBot/blob/Pyrogram/COPYING>.

import os
import subprocess
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import Message
from bot import (
    AUTHORIZED_CHATS
)
from bot.helper.telegram_helper.bot_commands import BotCommands


@Client.on_message(
    filters.command(BotCommands.ExecCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def execution_cmd_t(client, message: Message):
    PROCESS_RUNNING = "..."
    # send a message, use it to update the progress when required
    status_message = message.reply_text(PROCESS_RUNNING, quote=True)
    # get the message from the triggered command
    cmd = message.text.split(" ", maxsplit=1)[1]

    process = subprocess.run(
        cmd.split(" "),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    e_ = process.stderr.decode()
    if not e_:
        e_ = "No Error"
    o_ = process.stdout.decode()
    if not o_:
        o_ = "No Output"
    r_c = process.returncode
    
    final_output = f"<b>command</b>: <code>{cmd}</code>\n\n<b>stderr</b>: \n<code>{e_}</code>\n\n<b>stdout</b>: \n<code>{o_}</code>\n\n<b>return</b>: <code>{r_c}</code>"

    if len(final_output) > 4095:
        with open("eval.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        status_message.reply_document(
            document="eval.text",
            caption=cmd,
            disable_notification=True
        )
        os.remove("eval.text")
        status_message.delete()
    else:
        status_message.edit(final_output)
