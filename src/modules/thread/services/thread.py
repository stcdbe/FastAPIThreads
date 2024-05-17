from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from src.modules.thread.models.entities import Thread
from src.modules.thread.repositories.base import AbstractThreadRepository
from src.modules.thread.repositories.mongo import MongoThreadRepository
from src.modules.thread.views.schemas import ThreadCreate


class ThreadService:
    _repository: AbstractThreadRepository

    def __init__(self, repository: Annotated[AbstractThreadRepository, Depends(MongoThreadRepository)]) -> None:
        self._repository = repository

    async def get_list(self, params: dict[str, Any]) -> list[Thread]:
        return await self._repository.get_list(
            offset=params["offset"],
            limit=params["limit"],
            order_by=params["ordering"],
            reverse=params["reverse"],
        )

    async def get_one(self, guid: UUID) -> Thread | None:
        return await self._repository.get_one(guid=guid)

    async def create_one(self, thread_data: ThreadCreate) -> Thread:
        thread = Thread(**thread_data.model_dump())
        await self._repository.create_one(thread=thread)
        return thread

    async def delete_one(self, thread: Thread) -> None:
        await self._repository.delete_one(thread=thread)
