from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from src.database.dbmodels import UserDB
from src.user.userschemas import UserCreate, UserPatch

from src.auth.hasher import Hasher


async def get_user_db(user_id: PydanticObjectId) -> UserDB | None:
    return await UserDB.find_one(UserDB.id == user_id)


async def get_user_by_username_db(username: str) -> UserDB | None:
    return await UserDB.find_one(UserDB.username == username)


async def get_some_users_db(offset: int,
                            limit: int,
                            ordering: str,
                            reverse: bool) -> list[UserDB]:
    users = await UserDB.find_all().skip(offset).limit(limit).sort(ordering).to_list()

    if reverse:
        users = users[::-1]

    return users


async def create_user_db(user_data: UserCreate) -> UserDB | None:
    user_data.email = user_data.email.lower()
    user_data.password = Hasher.gen_psw_hash(psw=user_data.password)

    new_user = UserDB(**user_data.model_dump(mode='json'))

    try:
        return await UserDB.insert_one(new_user)
    except DuplicateKeyError:
        return


async def patch_user_db(user: UserDB, patch_data: UserPatch) -> UserDB | None:
    if patch_data.email:
        patch_data.email = patch_data.email.lower()
    if patch_data.password:
        patch_data.password = Hasher.gen_psw_hash(psw=patch_data.password)

    for key, val in patch_data.model_dump(exclude_none=True, exclude_unset=True).items():
        setattr(user, key, val)

    try:
        await user.replace()
        return user
    except (DuplicateKeyError, ValueError):
        return
