from typing import Any, Annotated

from fastapi import Depends

from src.auth.auth_utils import Hasher
from src.user.user_models import UserDB
from src.user.user_repositories import UserRepository
from src.user.user_schemas import UserCreate, UserPatch


class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]) -> None:
        self.user_repository = user_repository

    async def get_list(self, params: dict[str, Any]) -> list[UserDB]:
        offset = (params['page'] - 1) * params['limit']
        return await self.user_repository.get_list(offset=offset,
                                                   limit=params['limit'],
                                                   ordering=params['ordering'],
                                                   reverse=params['reverse'])

    async def get_one(self, **kwargs: Any) -> UserDB | None:
        return await self.user_repository.get_one(**kwargs)

    async def create_one(self, user_data: UserCreate) -> UserDB:
        user_data.email = user_data.email.lower()
        user_data.password = Hasher.gen_psw_hash(psw=user_data.password)

        new_user = UserDB(**user_data.model_dump(mode='json'))

        return await self.user_repository.create_one(new_user=new_user)

    async def patch_one(self, user: UserDB, patch_data: UserPatch) -> UserDB:
        if patch_data.email:
            patch_data.email = patch_data.email.lower()
        if patch_data.password:
            patch_data.password = Hasher.gen_psw_hash(psw=patch_data.password)

        for key, val in patch_data.model_dump(exclude_none=True, exclude_unset=True).items():
            setattr(user, key, val)

        return await self.user_repository.patch_one(user=user)
