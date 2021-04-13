#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
# 🙏🙏🦾 please 🤕 keep 🤕 the 🤒 credits 🙏👊
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
from pyrogram import Client
from pyrogram.types import (
    Message
)
from time import sleep
from typing import List
from bot import download_dict, DOWNLOAD_DIR
from bot.helper.ext_utils.fs_utils import clean_download
from bot.helper.telegram_helper.message_utils import *


@Client.on_deleted_messages()
def on_del_mesgs(client: Client, messages: List[Message]):
    # a a w t c m d
    for message in messages:
        # n s r t y e c s
        dl = download_dict.get(message.message_id)
        if dl:
            # d r h b v d c
            if dl.status() == "Uploading":
                sendMessage(
                    "Upload in Progress, Can't Cancel it, .",
                    client,
                    message
                )
                return
            elif dl.status() == "Archiving":
                sendMessage(
                    "Archival in Progress, Can't Cancel it, .",
                    client,
                    message
                )
                return
            else:
                dl.download().cancel_download()
            # c d t s p h r n s t p
            # d t d d t t a h
            sleep(1)
            # Wait a Second For Aria2 To free Resources.
            clean_download(
                os.path.join(
                    DOWNLOAD_DIR,
                    str(message.message_id)
                ) + os.path.sep
            )
    # 🙏🙏 k l q a o p 🙏🙏

