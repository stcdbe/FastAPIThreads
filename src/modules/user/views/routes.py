from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from src.modules.auth.dependencies import CurrentUserDep
from src.modules.user.dependencies import UserServiceDep, get_user_list_params, validate_user_guid
from src.modules.user.exceptions.exceptions import InvalidUserDataError
from src.modules.user.models.entities import User
from src.modules.user.views.schemas import UserCreate, UserGet, UserPatch

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post(
    path="",
    status_code=201,
    response_model=UserGet,
    name="Create a new user",
)
async def create_user(user_service: UserServiceDep, data: UserCreate) -> User:
    try:
        return await user_service.create_one(data=data)
    except InvalidUserDataError as exc:
        raise HTTPException(status_code=409, detail=exc.message) from exc


@user_router.get(
    path="",
    status_code=200,
    response_model=list[UserGet],
    name="Get some users",
)
async def get_some_users(
    _: CurrentUserDep,
    user_service: UserServiceDep,
    params: Annotated[dict[str, Any], Depends(get_user_list_params)],
) -> list[User]:
    return await user_service.get_list(params=params)


@user_router.get(
    path="/me",
    status_code=200,
    response_model=UserGet,
    name="Get the current user",
)
async def get_me(current_user: CurrentUserDep) -> User:
    return current_user


@user_router.patch(
    path="/me",
    status_code=200,
    response_model=UserGet,
    name="Patch the current user",
)
async def patch_me(
    current_user: CurrentUserDep,
    user_service: UserServiceDep,
    data: UserPatch,
) -> User:
    return await user_service.patch_one(user=current_user, data=data)


@user_router.get(
    path="/{guid}",
    status_code=200,
    response_model=UserGet,
    name="Get the user",
)
async def get_user(
    _: CurrentUserDep,
    user: Annotated[User, Depends(validate_user_guid)],
) -> User:
    return user
