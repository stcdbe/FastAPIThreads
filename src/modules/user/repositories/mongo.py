from collections.abc import Mapping
from typing import Annotated, Any

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import DESCENDING

from src.core.database.mongo import get_user_collection
from src.modules.user.models.entities import User
from src.modules.user.repositories.base import AbstractUserRepository
from src.modules.user.repositories.converters import convert_user_doc_to_entity


class MongoUserRepository(AbstractUserRepository):
    def __init__(self, collection: Annotated[AsyncIOMotorCollection, Depends(get_user_collection)]) -> None:
        self._collection = collection

    async def count(self, **kwargs: Any) -> int:
        return await self._collection.count_documents(filter=kwargs)

    async def get_list(self, offset: int, limit: int, order_by: str, reverse: bool = False) -> list[User]:
        if reverse:
            order_by = ((order_by, DESCENDING),)

        cursor = self._collection.find().skip(skip=offset).limit(limit=limit).sort(key_or_list=order_by)

        return [convert_user_doc_to_entity(data=doc) async for doc in cursor]

    async def get_one(self, **kwargs: Any) -> User | None:
        doc = await self._collection.find_one(filter=kwargs)
        if doc is not None:
            return convert_user_doc_to_entity(data=doc)
        return None

    async def create_one(self, user: User) -> None:
        await self._collection.insert_one(document=user.dump_to_dict())

    async def patch_one(self, user: User, data: Mapping[str, Any]) -> None:
        await self._collection.find_one_and_update(filter={"guid": user.guid}, update={"$set": data})
