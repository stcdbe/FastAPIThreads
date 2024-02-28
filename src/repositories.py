from abc import ABC, abstractmethod
from typing import Any, NoReturn


class AbstractRepository(ABC):
    @abstractmethod
    async def get_list(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def create_one(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def patch_one(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError


class MongoRepository(AbstractRepository, ABC):
    pass
