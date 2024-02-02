from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.config import settings
from src.user.usermodels import UserDB
from src.thread.threadmodels import ThreadDB


async def init_db() -> None:
    mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(database=mongo_client[settings.MONGO_DB], document_models=[UserDB, ThreadDB])
