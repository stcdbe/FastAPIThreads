from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from src.modules.thread.models.entities import Comment, Thread


class AbstractThreadRepository(ABC):
    @abstractmethod
    async def get_list(self, offset: int, limit: int, order_by: str, reverse: bool = False) -> list[Thread]: ...

    @abstractmethod
    async def get_one(self, **kwargs: Any) -> Thread | None: ...

    @abstractmethod
    async def create_one(self, thread: Thread) -> None: ...

    @abstractmethod
    async def patch_one(self, thread: Thread, data: Mapping[str, Any]) -> None: ...

    @abstractmethod
    async def add_comment(self, thread: Thread, comment: Comment) -> None: ...

    @abstractmethod
    async def delete_one(self, thread: Thread) -> None: ...
