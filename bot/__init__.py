import logging
import os
import threading
import time
import random
import string

import aria2p
import telegram.ext as tg
from dotenv import load_dotenv

import socket
from megasdkrestclient import MegaSdkRestClient, errors as mega_err
import subprocess

import psycopg2
from psycopg2 import Error

socket.setdefaulttimeout(600)

botStartTime = time.time()
if os.path.exists("log.txt"):
    with open("log.txt", "r+") as f:
        f.truncate(0)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

load_dotenv("config.env")

Interval = []


def getConfig(name: str):
    return os.environ[name]


def mktable():
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        sql = "CREATE TABLE users (uid bigint, sudo boolean DEFAULT FALSE);"
        cur.execute(sql)
        conn.commit()
        LOGGER.info("Table Created!")
    except Error as e:
        LOGGER.error(e)
        exit(1)


try:
    if bool(getConfig("_____REMOVE_THIS_LINE_____")):
        logging.error("The README.md file there to be read! Exiting now!")
        exit()
except KeyError:
    pass

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
# Key: update.effective_chat.id
# Value: telegram.Message
status_reply_dict = {}
# Key: update.message.message_id
# Value: An object of Status
download_dict = {}
# Stores list of users and chats the bot is authorized to use in
AUTHORIZED_CHATS = set()
SUDO_USERS = set()

try:
    CREDENTIALS = getConfig("CREDENTIALS")
    BOT_TOKEN = getConfig("BOT_TOKEN")
    DB_URI = getConfig("DATABASE_URL")
    parent_id = getConfig("GDRIVE_FOLDER_ID")
    DOWNLOAD_DIR = getConfig("DOWNLOAD_DIR")
    if DOWNLOAD_DIR[-1] != "/" or DOWNLOAD_DIR[-1] != "\\":
        DOWNLOAD_DIR = DOWNLOAD_DIR + "/"
    DOWNLOAD_STATUS_UPDATE_INTERVAL = int(getConfig("DOWNLOAD_STATUS_UPDATE_INTERVAL"))
    OWNER_ID = int(getConfig("OWNER_ID"))
    AUTO_DELETE_MESSAGE_DURATION = int(getConfig("AUTO_DELETE_MESSAGE_DURATION"))
    TELEGRAM_API = getConfig("TELEGRAM_API")
    TELEGRAM_HASH = getConfig("TELEGRAM_HASH")
except KeyError as e:
    LOGGER.error("One or more env variables missing! Exiting now")
    exit(1)

try:
    HEROKU_API_KEY = getConfig("HEROKU_API_KEY")
    HEROKU_APP_NAME = getConfig("HEROKU_APP_NAME")
except BaseException:
    HEROKU_API_KEY = None
    HEROKU_APP_NAME = None
    logging.warning("Heroku vars is not provided or Invalid!")

try:
    conn = psycopg2.connect(DB_URI)
    cur = conn.cursor()
    sql = "SELECT * from users;"
    cur.execute(sql)
    rows = cur.fetchall()  # returns a list ==> (uid, sudo)
    for row in rows:
        AUTHORIZED_CHATS.add(row[0])
        if row[1]:
            SUDO_USERS.add(row[0])
except Error as e:
    if 'relation "users" does not exist' in str(e):
        mktable()
    else:
        LOGGER.error(e)
        exit(1)
finally:
    cur.close()
    conn.close()

try:
    MEGA_KEY = getConfig("MEGA_KEY")
except KeyError:
    MEGA_KEY = None
    LOGGER.info("MEGA API KEY NOT AVAILABLE")
if MEGA_KEY is not None:
    try:
        MEGA_USERNAME = getConfig("MEGA_USERNAME")
        MEGA_PASSWORD = getConfig("MEGA_PASSWORD")
        # Start megasdkrest binary
        subprocess.Popen(["megasdkrest", "--apikey", MEGA_KEY])
        time.sleep(3)
        mega_client = MegaSdkRestClient("http://localhost:6090")
        try:
            mega_client.login(MEGA_USERNAME, MEGA_PASSWORD)
        except mega_err.MegaSdkRestClientException as e:
            logging.error(e.message["message"])
            exit(0)
    except KeyError:
        LOGGER.info(
            "Mega API KEY provided but credentials not provided. Starting mega in anonymous mode!"
        )
        MEGA_USERNAME = None
        MEGA_PASSWORD = None
else:
    MEGA_USERNAME = None
    MEGA_PASSWORD = None

try:
    INDEX_URL = getConfig("INDEX_URL")
    if len(INDEX_URL) == 0:
        INDEX_URL = None
except KeyError:
    INDEX_URL = None
try:
    IS_TEAM_DRIVE = getConfig("IS_TEAM_DRIVE")
    if IS_TEAM_DRIVE.lower() == "true":
        IS_TEAM_DRIVE = True
    else:
        IS_TEAM_DRIVE = False
except KeyError:
    IS_TEAM_DRIVE = False

try:
    USE_SERVICE_ACCOUNTS = getConfig("USE_SERVICE_ACCOUNTS")
    if USE_SERVICE_ACCOUNTS.lower() == "true":
        USE_SERVICE_ACCOUNTS = True
    else:
        USE_SERVICE_ACCOUNTS = False
except KeyError:
    USE_SERVICE_ACCOUNTS = False

updater = tg.Updater(token=BOT_TOKEN, use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher
