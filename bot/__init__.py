import logging
import os
import threading
import time

import aria2p
from .get_config import getConfig
from dotenv import load_dotenv
import socket

socket.setdefaulttimeout(600)

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('log.txt'),
        logging.StreamHandler()
    ],
    level=logging.INFO
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


if os.path.exists("config.env"):
    load_dotenv('config.env')
else:
    load_dotenv('config_sample.env')

Interval = []

LOGGER = logging.getLogger(__name__)

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret="",
    )
)

DOWNLOAD_DIR = None
BOT_TOKEN = None

download_dict_lock = threading.Lock()
status_reply_dict_lock = threading.Lock()
# Key: message.chat.id
# Value: telegram.Message
status_reply_dict = {}
# Key: message.message_id
# Value: An object of Status
download_dict = {}


BOT_TOKEN = getConfig('BOT_TOKEN', should_prompt=True)
parent_id = getConfig('GDRIVE_FOLDER_ID')
DOWNLOAD_DIR = getConfig('DOWNLOAD_DIR')
DOWNLOAD_DIR = os.path.abspath(DOWNLOAD_DIR)
if DOWNLOAD_DIR[-1] != '/' or DOWNLOAD_DIR[-1] != '\\':
    DOWNLOAD_DIR = DOWNLOAD_DIR + os.path.sep
DOWNLOAD_STATUS_UPDATE_INTERVAL = int(getConfig(
    'DOWNLOAD_STATUS_UPDATE_INTERVAL'
))
OWNER_ID = int(getConfig('OWNER_ID', should_prompt=True))
AUTO_DELETE_MESSAGE_DURATION = int(getConfig('AUTO_DELETE_MESSAGE_DURATION'))
TELEGRAM_API = getConfig('TELEGRAM_API', should_prompt=True)
TELEGRAM_HASH = getConfig('TELEGRAM_HASH', should_prompt=True)
CRED_JSON = getConfig('CRED_JSON')

# Stores list of users and chats the bot is authorized to use in
AUTHORIZED_CHATS = set(
    int(x) for x in getConfig("AUTHORIZED_CHATS", should_prompt=True).split()
)
AUTHORIZED_CHATS = list(AUTHORIZED_CHATS)
AUTHORIZED_CHATS.append(OWNER_ID)
AUTHORIZED_CHATS = list(set(AUTHORIZED_CHATS))

MEGA_API_KEY = getConfig('MEGA_API_KEY', None)

MEGA_EMAIL_ID = getConfig('MEGA_EMAIL_ID', None)
MEGA_PASSWORD = getConfig('MEGA_PASSWORD', None)

USE_SERVICE_ACCOUNTS = bool(getConfig('USE_SERVICE_ACCOUNTS', None))

INDEX_URL = getConfig('INDEX_URL', None)
IS_TEAM_DRIVE = bool(getConfig('IS_TEAM_DRIVE', None))
