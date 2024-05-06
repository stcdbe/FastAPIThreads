from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from src.modules.user.models.entities import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def count(self, **kwargs: Any) -> int: ...

    @abstractmethod
    async def get_list(self, offset: int, limit: int, order_by: str, reverse: bool = False) -> list[User]: ...

    @abstractmethod
    async def get_one(self, **kwargs: Any) -> User | None: ...

    @abstractmethod
    async def create_one(self, user: User) -> None: ...

    @abstractmethod
    async def patch_one(self, user: User, data: Mapping[str, Any]) -> None: ...
