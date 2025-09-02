from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database.database import Database

db = Database()

@Client.on_message(filters.channel & filters.document)
async def save_file(_, message: Message):
    file = message.document
    if not file:
        return
    await db.add_file(file.file_id, file.file_name or "Unnamed")
