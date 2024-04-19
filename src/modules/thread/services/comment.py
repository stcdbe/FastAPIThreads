from typing import Annotated

from fastapi import Depends

from src.modules.thread.models.entities import Thread, Comment
from src.modules.thread.repositories.base import AbstractThreadRepository
from src.modules.thread.repositories.mongo import MongoThreadRepository
from src.modules.thread.views.schemas import CommentCreate


class CommentService:
    def __init__(self, repository: Annotated[AbstractThreadRepository, Depends(MongoThreadRepository)]) -> None:
        self._repository = repository

    async def create_one(self, thread: Thread, data: CommentCreate) -> Thread:
        if len(thread.comments) == 99:
            thread.is_active = False
            await self._repository.patch_one(thread=thread, data={'is_active': False})

        com = Comment(**data.model_dump())
        thread.comments.append(com)
        await self._repository.add_comment(thread=thread, comment=com)

        return thread
