from typing import Any, Annotated

from fastapi import Depends

from src.thread.thread_models import ThreadDB
from src.thread.thread_repositories import ThreadRepository
from src.thread.thread_schemas import CommentCreate, CommentGet, ThreadCreate


class ThreadService:
    def __init__(self, thread_repository: Annotated[ThreadRepository, Depends()]) -> None:
        self.thread_repository = thread_repository

    async def get_list(self, params: dict[str, Any]) -> list[ThreadDB]:
        offset = (params['page'] - 1) * params['limit']
        return await self.thread_repository.get_list(offset=offset,
                                                     limit=params['limit'],
                                                     ordering=params['ordering'],
                                                     reverse=params['reverse'])

    async def get_one(self, **kwargs: Any) -> ThreadDB | None:
        return await self.thread_repository.get_one(**kwargs)

    async def create_one(self, thread_data: ThreadCreate) -> ThreadDB:
        new_thread = ThreadDB(**thread_data.model_dump(mode='json'))
        return await self.thread_repository.create_one(new_thread=new_thread)

    async def del_one(self, thread: ThreadDB) -> None:
        await self.thread_repository.del_one(thread=thread)


class CommentService:
    def __init__(self, thread_repository: Annotated[ThreadRepository, Depends()]) -> None:
        self.thread_repository = thread_repository

    async def create_one(self, thread: ThreadDB, com_data: CommentCreate) -> ThreadDB:
        if len(thread.comments) == 99:
            thread.is_active = False

        new_com = CommentGet(**com_data.model_dump(mode='json'))
        thread.comments.append(new_com)
        return await self.thread_repository.patch_one(thread=thread)
