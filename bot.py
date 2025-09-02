import logging
from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Adv-Auto-Filter-Bot",
            bot_token=BOT_TOKEN,
            api_id=API_ID,
            api_hash=API_HASH,
            plugins=dict(root="bot.plugins")
        )

if __name__ == "__main__":
    Bot().run()
