from typing import AsyncGenerator, Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from src.config import settings

mongo_client = AsyncIOMotorClient(settings.MONGO_URL, uuidRepresentation="standard")

mongo_db = mongo_client[settings.MONGO_DB]


async def get_user_collection() -> AsyncGenerator[AsyncIOMotorCollection, Any]:
    yield mongo_db[settings.MONGO_USER_COLLECTION]


async def get_thread_collection() -> AsyncGenerator[AsyncIOMotorCollection, Any]:
    yield mongo_db[settings.MONGO_THREAD_COLLECTION]
