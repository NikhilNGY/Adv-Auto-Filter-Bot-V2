import os
import logging
from logging.handlers import RotatingFileHandler

# Get a bot token from botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Get from my.telegram.org
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")

# Your database URL from mongoDB
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# The channel ID of a logging channel
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))

# Your user session string. Get it from @StringGenBot
USER_SESSION_STRING = os.environ.get("USER_SESSION_STRING", "")

# ID of users who can use admin commands
# For multiple admins, separate IDs with a space
ADMINS = [int(admin) for admin in os.environ.get("ADMINS", "").split()]

# A force subscription channel or group ID
# Leave 0 if you don't want to use this feature
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", 0))

# Set this to True if you want to prevent users from sharing files from your bot
PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False").lower() == "true"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler("bot.log", maxBytes=5000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

# Verify essential configurations
if not BOT_TOKEN:
    LOGGER.critical("BOT_TOKEN is not set. Exiting...")
    exit(1)
if not API_ID or not API_HASH:
    LOGGER.critical("API_ID or API_HASH is not set. Exiting...")
    exit(1)
if not DATABASE_URI:
    LOGGER.critical("DATABASE_URI is not set. Exiting...")
    exit(1)
if not USER_SESSION_STRING:
    LOGGER.warning("USER_SESSION_STRING is not set. The bot may not work as a user.")
