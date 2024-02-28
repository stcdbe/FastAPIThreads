from typing import Any

from fastapi import HTTPException
from pymongo import DESCENDING
from pymongo.errors import DuplicateKeyError

from src.repositories import MongoRepository
from src.user.user_models import UserDB


class UserRepository(MongoRepository):
    async def get_list(self,
                       offset: int,
                       limit: int,
                       ordering: str,
                       reverse: bool = False) -> list[UserDB]:
        if reverse:
            ordering = (ordering, DESCENDING)

        return await UserDB.find_all().skip(offset).limit(limit).sort(ordering).to_list()

    async def get_one(self, **kwargs: Any) -> UserDB | None:
        return await UserDB.find(kwargs).first_or_none()

    async def create_one(self, new_user: UserDB) -> UserDB:
        try:
            return await UserDB.insert_one(new_user)
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail='The user with this username or email already exists')

    async def patch_one(self, user: UserDB) -> UserDB:
        try:
            await user.replace()

        except (DuplicateKeyError, ValueError):
            raise HTTPException(status_code=409, detail='The user with this username or email already exists')

        else:
            return user
