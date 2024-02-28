from typing import Annotated, Any

from fastapi import APIRouter, Depends

from src.auth.auth_dependencies import CurrentUserDep
from src.user.user_dependencies import validate_user_id, get_user_list_params, UserServiceDep
from src.user.user_models import UserDB
from src.user.user_schemas import UserCreate, UserGet, UserPatch

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post(path='',
                  status_code=201,
                  response_model=UserGet,
                  name='Create a new user')
async def create_user(user_service: UserServiceDep, user_data: UserCreate) -> UserDB:
    return await user_service.create_one(user_data=user_data)


@user_router.get(path='',
                 status_code=200,
                 response_model=list[UserGet],
                 name='Get some users')
async def get_some_users(current_user: CurrentUserDep,
                         user_service: UserServiceDep,
                         params: Annotated[dict[str, Any], Depends(get_user_list_params)]) -> list[UserDB]:
    return await user_service.get_list(params=params)


@user_router.get(path='/me',
                 status_code=200,
                 response_model=UserGet,
                 name='Get the current user')
async def get_me(current_user: CurrentUserDep) -> UserDB:
    return current_user


@user_router.patch(path='/me',
                   status_code=200,
                   response_model=UserGet,
                   name='Patch the current user')
async def patch_me(current_user: CurrentUserDep,
                   user_service: UserServiceDep,
                   patch_data: UserPatch) -> UserDB:
    return await user_service.patch_one(user=current_user, patch_data=patch_data)


@user_router.get(path='/{user_id}',
                 status_code=200,
                 response_model=UserGet,
                 name='Get the user')
async def get_user(current_user: CurrentUserDep, user: Annotated[UserDB, Depends(validate_user_id)]) -> UserDB:
    return user
