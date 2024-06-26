from collections.abc import Mapping
from typing import Annotated, Any

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import DESCENDING

from src.core.database.mongo import get_thread_collection
from src.modules.thread.models.entities import Comment, Thread
from src.modules.thread.repositories.base import AbstractThreadRepository
from src.modules.thread.repositories.converters import (
    convert_thread_doc_to_entity,
    convert_thread_doc_to_entity_with_coms,
)


class MongoThreadRepository(AbstractThreadRepository):
    _collection: AsyncIOMotorCollection

    def __init__(self, collection: Annotated[AsyncIOMotorCollection, Depends(get_thread_collection)]) -> None:
        self._collection = collection

    async def get_list(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool = False,
    ) -> list[Thread]:
        if reverse:
            order_by = ((order_by, DESCENDING),)

        cursor = self._collection.find().skip(skip=offset).limit(limit=limit).sort(key_or_list=order_by)

        return [convert_thread_doc_to_entity(data=doc) async for doc in cursor]

    async def get_one(self, **kwargs: Any) -> Thread | None:
        doc = await self._collection.find_one(filter=kwargs)
        if doc is not None:
            return convert_thread_doc_to_entity_with_coms(data=doc)
        return None

    async def create_one(self, thread: Thread) -> None:
        await self._collection.insert_one(document=thread.dump_to_dict())

    async def patch_one(self, thread: Thread, data: Mapping[str, Any]) -> None:
        await self._collection.find_one_and_update(filter={"guid": thread.guid}, update={"$set": data})

    async def add_comment(self, thread: Thread, comment: Comment) -> None:
        await self._collection.update_one(
            filter={"guid": thread.guid},
            update={"$push": {"comments": comment.dump_to_dict()}},
        )

    async def delete_one(self, thread: Thread) -> None:
        await self._collection.delete_one(filter={"guid": thread.guid})
        del thread
