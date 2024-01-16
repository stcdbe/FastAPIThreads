from typing import Annotated, Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from src.auth.authutils import get_current_user
from src.database.dbmodels import UserDB
from src.user.userschemas import UserCreate, UserGet, UserPatch
from src.user.userservice import create_user_db, get_some_users_db, get_user_db, patch_user_db


user_router = APIRouter()


@user_router.post('',
                  status_code=201,
                  response_model=UserGet,
                  name='Create a new user')
async def create_user(user_data: UserCreate) -> Any:
    new_user = await create_user_db(user_data=user_data)

    if not new_user:
        raise HTTPException(status_code=409, detail='The user with this username or email already exists')

    return new_user


@user_router.get('',
                 status_code=200,
                 response_model=list[UserGet],
                 name='Get some users')
async def get_some_users(current_user: Annotated[UserDB, Depends(get_current_user)],
                         page: Annotated[int, Query(gt=0)] = 1,
                         limit: Annotated[int, Query(gt=0, le=10)] = 5,
                         ordering: Annotated[str, Query(enum=list(UserGet.model_fields))] = 'username',
                         reverse: bool = False) -> Any:
    offset = (page - 1) * limit
    return await get_some_users_db(offset=offset,
                                   limit=limit,
                                   ordering=ordering,
                                   reverse=reverse)


@user_router.get('/me',
                 status_code=200,
                 response_model=UserGet,
                 name='Get the current user')
async def get_me(current_user: Annotated[UserDB, Depends(get_current_user)]) -> Any:
    return current_user


@user_router.patch('/me',
                   status_code=200,
                   response_model=UserGet,
                   name='Patch the current user')
async def patch_me(current_user: Annotated[UserDB, Depends(get_current_user)],
                   patch_data: UserPatch) -> Any:
    upd_user = await patch_user_db(user=current_user, patch_data=patch_data)

    if not upd_user:
        raise HTTPException(status_code=409, detail='The user with this username or email already exists')

    return upd_user


@user_router.get('/{user_id}',
                 status_code=200,
                 response_model=UserGet,
                 name='Get the user')
async def get_user(current_user: Annotated[UserDB, Depends(get_current_user)],
                   user_id: PydanticObjectId) -> Any:
    user = await get_user_db(user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail='Not found')

    return user
