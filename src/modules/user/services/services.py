from typing import Any, Annotated

from fastapi import Depends

from src.modules.auth.utils.hasher import Hasher
from src.modules.user.exceptions.exceptions import InvalidUserDataError
from src.modules.user.models.entities import User
from src.modules.user.repositories.base import AbstractUserRepository
from src.modules.user.repositories.mongo import MongoUserRepository
from src.modules.user.views.schemas import UserCreate, UserPatch


class UserService:
    def __init__(self, repository: Annotated[AbstractUserRepository, Depends(MongoUserRepository)]) -> None:
        self._repository = repository

    async def get_list(self, params: dict[str, Any]) -> list[User]:
        return await self._repository.get_list(offset=params['offset'],
                                               limit=params['limit'],
                                               order_by=params['ordering'],
                                               reverse=params['reverse'])

    async def get_one(self, **kwargs: Any) -> User | None:
        return await self._repository.get_one(**kwargs)

    async def create_one(self, data: UserCreate) -> User:
        data.email = data.email.lower()

        if bool(await self._repository.count(username=data.username)):
            raise InvalidUserDataError('Username must be unique')

        if bool(await self._repository.count(email=data.email)):
            raise InvalidUserDataError('Email must be unique')

        data.password = Hasher.gen_psw_hash(psw=data.password)

        user = User(**data.model_dump())

        await self._repository.create_one(user=user)

        return user

    async def patch_one(self, user: User, data: UserPatch) -> User:
        if data.email:
            data.email = data.email.lower()
        if data.password:
            data.password = Hasher.gen_psw_hash(psw=data.password)

        dump = data.model_dump(exclude_none=True, exclude_unset=True)

        for key, val in dump.items():
            setattr(user, key, val)

        await self._repository.patch_one(user=user, data=dump)

        return user
