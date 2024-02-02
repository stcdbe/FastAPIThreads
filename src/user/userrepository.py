from typing import Any

from pymongo import DESCENDING
from pymongo.errors import DuplicateKeyError

from src.repository import AbstractRepository
from src.user.usermodels import UserDB


class UserRepository(AbstractRepository):
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

    async def create_one(self, new_user: UserDB) -> UserDB | None:
        try:
            return await UserDB.insert_one(new_user)
        except DuplicateKeyError:
            return

    async def patch_one(self, user: UserDB) -> UserDB | None:
        try:
            await user.replace()
            return user
        except (DuplicateKeyError, ValueError):
            return
