#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://github.com/SpEcHiDe/TerminalBot/blob/Pyrogram/COPYING>.

import io
import os
import sys
import traceback

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
    filters.command(BotCommands.EvalCommand) &
    filters.chat(AUTHORIZED_CHATS)
)
def evaluation_cmd_t(client, message: Message):
    PROCESS_RUNNING = "..."
    status_message = message.reply_text(PROCESS_RUNNING, quote=True)

    cmd = message.text.split(" ", maxsplit=1)[1]

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "😐"

    final_output = "<b>EVAL</b>: <code>{}</code>\n\n<b>OUTPUT</b>:\n<code>{}</code>".format(
        cmd, evaluation.strip()
    )

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


def aexec(code, client, message):
    exec(
        f'def __aexec(client, message): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return locals()['__aexec'](client, message)
