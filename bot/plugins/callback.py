from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

@Client.on_callback_query()
async def handle_callback(_, query: CallbackQuery):
    await query.answer("This is a placeholder callback response.", show_alert=True)
