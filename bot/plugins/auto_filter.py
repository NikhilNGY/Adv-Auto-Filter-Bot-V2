from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database.database import Database
from config import RESULTS_COUNT

db = Database()

@Client.on_message(filters.text & filters.group)
async def auto_filter(_, message: Message):
    query = message.text.strip()
    results = await db.search_files(query, RESULTS_COUNT)

    if not results:
        return

    response = "\n".join(
        [f"📂 {r['name']} — <code>{r['file_id']}</code>" for r in results]
    )
    await message.reply(response, quote=True)
