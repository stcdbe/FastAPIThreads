from collections.abc import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from src.config import settings

test_mongo_client = AsyncIOMotorClient(settings.MONGO_URL_TEST, uuidRepresentation="standard")
test_mongo_db = test_mongo_client[settings.MONGO_DB_TEST]


async def get_test_user_collection() -> AsyncGenerator[AsyncIOMotorCollection, None]:
    yield test_mongo_db[settings.MONGO_USER_COLLECTION_TEST]


async def get_test_thread_collection() -> AsyncGenerator[AsyncIOMotorCollection, None]:
    yield test_mongo_db[settings.MONGO_THREAD_COLLECTION_TEST]


async def clear_mongo_collections() -> None:
    await test_mongo_db.drop_collection(name_or_collection=settings.MONGO_USER_COLLECTION)
    await test_mongo_db.drop_collection(name_or_collection=settings.MONGO_THREAD_COLLECTION)
