import os
import re
import logging
from logging.handlers import RotatingFileHandler

# Telegram Bot credentials
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", "2468192"))  # Your API ID from my.telegram.org
API_HASH = os.environ.get("API_HASH", "4906b3f8f198ec0e24edb2c197677678")  # Your API Hash from my.telegram.org

# Database config
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "Filter2")

# ✅ Regex to check if admin is an integer ID
id_pattern = re.compile(r'^\d+$')

# Admins can be Telegram IDs or usernames
ADMINS = [
    int(admin) if id_pattern.match(admin) else admin
    for admin in os.environ.get("ADMINS", "").split()
]

# Server port (for render/railway)
PORT = int(os.environ.get("PORT", 8080))

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("bot.log", maxBytes=5_000_000, backupCount=2),
        logging.StreamHandler()
    ]
)
LOGGER = logging.getLogger(__name__)
