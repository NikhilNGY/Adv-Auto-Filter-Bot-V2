import motor.motor_asyncio
from config import DATABASE_URL

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
        self.db = self.client.auto_filter_bot

    # Admins
    async def get_admins(self, chat_id: int) -> list[int]:
        data = await self.db.admins.find_one({"chat_id": chat_id}) or {}
        return data.get("user_ids", [])

    async def add_admin(self, chat_id: int, user_id: int):
        await self.db.admins.update_one(
            {"chat_id": chat_id},
            {"$addToSet": {"user_ids": user_id}},
            upsert=True
        )

    async def remove_admin(self, chat_id: int, user_id: int):
        await self.db.admins.update_one(
            {"chat_id": chat_id},
            {"$pull": {"user_ids": user_id}},
            upsert=True
        )

    # Settings
    async def get_setting(self, chat_id: int, key: str, default=None):
        data = await self.db.settings.find_one({"chat_id": chat_id}) or {}
        return data.get(key, default)

    async def set_setting(self, chat_id: int, key: str, value):
        await self.db.settings.update_one(
            {"chat_id": chat_id},
            {"$set": {key: value}},
            upsert=True
        )

    # Files (simplified for auto-filter)
    async def add_file(self, file_id: str, name: str):
        await self.db.files.update_one(
            {"file_id": file_id},
            {"$set": {"name": name}},
            upsert=True
        )

    async def search_files(self, query: str, limit: int = 5):
        cursor = self.db.files.find({"name": {"$regex": query, "$options": "i"}}).limit(limit)
        return [doc async for doc in cursor]
