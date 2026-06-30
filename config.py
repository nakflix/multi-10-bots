#(©)t.me/Ahjin_Sprt
# Multi-bot config - run up to 10 bots from one codebase.
# Every bot shares the SAME settings below EXCEPT:
#   - Bot Token   (BOT{N}_TOKEN)
#   - MongoDB URI (BOT{N}_DB_URI)
#   - MongoDB DB name (BOT{N}_DB_NAME)

import os
import logging
from logging.handlers import RotatingFileHandler

# ---------------------------------------------------------------------------
# SHARED SETTINGS (same for all 10 bots)
# ---------------------------------------------------------------------------

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "14298205"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "28df6d84da76d8606bf5f0e71ecfb62c")

# Your database channel Id (where files are stored) - shared across all bots
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001755253960"))

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "1458235021"))

# Base port - each bot's web server binds to PORT, PORT+1, PORT+2, ... PORT+9
PORT = int(os.environ.get("PORT", "8080"))

# force sub channel ids, if you want enable force sub (shared across all bots)
FORCE_SUB_CHANNEL_1 = int(os.environ.get("FORCE_SUB_CHANNEL_1", "-1001899642588"))
FORCE_SUB_CHANNEL_2 = int(os.environ.get("FORCE_SUB_CHANNEL_2", "-1001849467785"))
FORCE_SUB_CHANNEL_3 = int(os.environ.get("FORCE_SUB_CHANNEL_3", "-1001855603689"))
FORCE_SUB_CHANNEL_4 = int(os.environ.get("FORCE_SUB_CHANNEL_4", "-1001895335215"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# start message
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello {first}\nI store private files for @NAKFLIXTV.</b>")

try:
    ADMINS = [5976081364]
    for x in (os.environ.get("ADMINS", "1458235021").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Force sub message
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "<b>Hello👋 {first}</b>\n<b>Kindly JOIN CHANNEL 1, 2, 3 and 4 Then press ♻️ Try Again ♻️ to continue. 👇</b>"
)

# set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "➥ 𝗩𝗜𝗦𝗜𝗧 & 𝗝𝗢𝗜𝗡 👉 @NAKFLIXTV")

# set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Send your request here 👉<a href='https://t.me/nakflix_bot?start='>@NAKFLIX_BOT</a>🤏"

ADMINS.append(OWNER_ID)
ADMINS.append(1737646273)

LOG_FILE_NAME = "logs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


# ---------------------------------------------------------------------------
# PER-BOT SETTINGS (these are the ONLY 3 things that differ between bots)
# ---------------------------------------------------------------------------
# Set these in your environment / .env file:
#   BOT1_TOKEN, BOT1_DB_URI, BOT1_DB_NAME
#   BOT2_TOKEN, BOT2_DB_URI, BOT2_DB_NAME
#   ...
#   BOT10_TOKEN, BOT10_DB_URI, BOT10_DB_NAME
#
# A bot slot is only started if its BOT{N}_TOKEN is set (non-empty).
# This means you can run anywhere from 1 to 10 bots just by filling in
# the slots you need.

MAX_BOTS = 10

BOTS = []
for i in range(1, MAX_BOTS + 1):
    token = os.environ.get(f"BOT{i}_TOKEN", "")
    if not token:
        continue
    BOTS.append({
        "name": f"Bot{i}",
        "token": token,
        "db_uri": os.environ.get(f"BOT{i}_DB_URI", ""),
        "db_name": os.environ.get(f"BOT{i}_DB_NAME", f"bot{i}_db"),
        "port": PORT + (i - 1),
    })

if not BOTS:
    raise Exception(
        "No bots configured! Set at least BOT1_TOKEN, BOT1_DB_URI, BOT1_DB_NAME "
        "in your environment to run a bot."
    )
