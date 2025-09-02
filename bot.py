import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")

if not all([API_ID, API_HASH, BOT_TOKEN, DATABASE_URL]):
    logger.error("Please set all required environment variables in the .env file.")
    exit()

# Pyrogram client
bot = Client(
    "auto_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# MongoDB client and database
db_client = AsyncIOMotorClient(DATABASE_URL)
db = db_client.auto_filter_db
files_collection = db.files

@bot.on_message(filters.media & filters.private)
async def save_media_to_db(client, message):
    """
    Saves media files (photos, videos, documents) sent in private chat to the database.
    """
    # The file_id is different for each media type, so we need to handle them
    file_id = None
    file_name = None
    if message.photo:
        file_id = message.photo.file_id
        file_name = message.caption or "Photo"
    elif message.video:
        file_id = message.video.file_id
        file_name = message.video.file_name or "Video"
    elif message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name or "Document"
    else:
        return

    try:
        # Check if the file already exists in the database
        existing_file = await files_collection.find_one({"file_id": file_id})
        if existing_file:
            await message.reply_text("This file is already in my database.")
            return

        # Save the file information to the database
        await files_collection.insert_one({
            "file_id": file_id,
            "file_name": file_name,
            "date": message.date,
            "caption": message.caption
        })

        await message.reply_text(f"Successfully saved file: `{file_name}`")
    except Exception as e:
        logger.error(f"Error saving file to database: {e}")
        await message.reply_text("Sorry, an error occurred while saving the file.")

@bot.on_inline_query()
async def search_files_inline(client, inline_query: InlineQuery):
    """
    Handles inline queries to search for files in the database.
    """
    query = inline_query.query.strip().lower()
    
    if not query:
        # If the query is empty, show a welcome message or some suggestions
        results = [
            InlineQueryResultArticle(
                title="Start searching!",
                description="Type the name of a file to search for it.",
                input_message_content=InputTextMessageContent(
                    message_text="Hello, I'm an auto-filter bot. Send me files to save them and use me in inline mode to search for them!"
                )
            )
        ]
        await inline_query.answer(results)
        return

    # Search the database for files matching the query
    cursor = files_collection.find({"file_name": {"$regex": query, "$options": "i"}}).limit(50)
    
    results = []
    async for file_doc in cursor:
        title = file_doc.get("file_name", "Unknown File")
        file_id = file_doc.get("file_id")
        
        # Create an inline button to send the file
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Get File", callback_data=f"get_{file_id}")]
        ])

        results.append(
            InlineQueryResultArticle(
                title=title,
                description=f"Click to get {title}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Searching for {title}..."
                ),
                reply_markup=keyboard
            )
        )
    
    # If no results found
    if not results:
        results.append(
            InlineQueryResultArticle(
                title="No results found",
                description=f"Sorry, I couldn't find any files matching '{query}'",
                input_message_content=InputTextMessageContent(
                    message_text=f"No results found for '{query}'"
                )
            )
        )

    await inline_query.answer(results, cache_time=1)

@bot.on_callback_query()
async def process_callback_query(client, callback_query):
    """
    Handles callback queries from inline buttons.
    """
    data = callback_query.data
    if data.startswith("get_"):
        file_id = data.replace("get_", "")
        try:
            # Send the file to the user
            await client.send_document(
                chat_id=callback_query.message.chat.id,
                document=file_id,
                caption="Here is the file you requested!"
            )
        except Exception as e:
            logger.error(f"Error sending file with ID {file_id}: {e}")
            await callback_query.answer("Failed to send the file. It may have been deleted.")
    else:
        await callback_query.answer("Invalid request!")

if __name__ == "__main__":
    bot.run()
