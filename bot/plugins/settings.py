from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database.database import Database
from helper_func import admin_filter

db = Database()

@Client.on_message(filters.command("set") & admin_filter)
async def set_setting(_, message: Message):
    if len(message.command) < 3:
        return await message.reply("Usage: /set <key> <value>")
    _, key, value = message.command
    await db.set_setting(message.chat.id, key, value)
    await message.reply(f"✅ Setting `{key}` updated to `{value}`")

@Client.on_message(filters.command("get") & admin_filter)
async def get_setting(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /get <key>")
    _, key = message.command
    value = await db.get_setting(message.chat.id, key, default="Not set")
    await message.reply(f"⚙️ {key} = {value}")
