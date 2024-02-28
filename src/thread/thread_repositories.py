from typing import Any

from pymongo import DESCENDING

from src.repositories import MongoRepository
from src.thread.thread_models import ThreadDB


class ThreadRepository(MongoRepository):
    async def get_list(self,
                       offset: int,
                       limit: int,
                       ordering: str,
                       reverse: bool = False) -> list[ThreadDB]:
        if reverse:
            ordering = (ordering, DESCENDING)

        return await ThreadDB.find_all().skip(offset).limit(limit).sort(ordering).to_list()

    async def get_one(self, **kwargs: Any) -> ThreadDB | None:
        return await ThreadDB.find(kwargs).first_or_none()

    async def create_one(self, new_thread: ThreadDB) -> ThreadDB:
        return await ThreadDB.insert_one(new_thread)

    async def patch_one(self, thread: ThreadDB) -> ThreadDB:
        await thread.replace()
        return thread

    async def del_one(self, thread: ThreadDB) -> None:
        await thread.delete()
