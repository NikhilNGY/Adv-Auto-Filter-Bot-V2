from pyrogram import filters
from pyrogram.types import Message
from bot.database.database import Database

db = Database()

async def check_admin(_, __, message: Message) -> bool:
    if not message.chat or not message.from_user:
        return False
    user_id = message.from_user.id
    admins = await db.get_admins(message.chat.id)
    return user_id in admins

admin_filter = filters.create(check_admin)
