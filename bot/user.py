from typing import Optional, Tuple
from pyrogram import Client
from .config import API_ID, API_HASH, USER_SESSION_STRING, LOGGER

class User(Client):
    """
    A Pyrogram client for the user account.
    """
    def __init__(self):
        super().__init__(
            "user_account",  # Renamed session name for clarity
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=USER_SESSION_STRING,
            no_updates=True,  # User account doesn't need to process updates
        )
        self.LOGGER = LOGGER

    async def start(self) -> Optional[Tuple['User', int]]:
        """
        Starts the user client and returns the client instance and user ID.
        """
        if not self.session_string:
            self.LOGGER(__name__).warning("USER_SESSION_STRING is not set. Skipping user client start.")
            return None, None
        
        await super().start()
        user_details = await self.get_me()
        self.LOGGER(__name__).info(
            f"User account started as @{user_details.username}."
        )
        return self, user_details.id

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("User client stopped.")
