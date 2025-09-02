import asyncio
from .bot import Bot
from .config import LOGGER

async def main():
    """
    The main entry point for the bot.
    Initializes and runs the bot client.
    """
    bot = Bot()
    try:
        LOGGER(__name__).info("Starting the bot...")
        await bot.start()
        # Keep the bot running indefinitely
        await asyncio.Event().wait()
    except Exception as e:
        LOGGER(__name__).error(f"An error occurred: {e}", exc_info=True)
    finally:
        LOGGER(__name__).info("Stopping the bot...")
        await bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER(__name__).info("Bot stopped by user.")
