from typing import Annotated, Any

from fastapi import Depends, HTTPException, Query
from pydantic import UUID4

from src.modules.user.models.entities import User
from src.modules.user.services.services import UserService
from src.modules.user.views.schemas import UserGet

UserServiceDep = Annotated[UserService, Depends()]


async def get_user_list_params(
    offset: Annotated[int, Query(ge=0, le=10)] = 0,
    limit: Annotated[int, Query(gt=0, le=10)] = 5,
    ordering: Annotated[str, Query(enum=tuple(UserGet.model_fields))] = "username",
    reverse: bool = False,
) -> dict[str, Any]:
    return {"offset": offset, "limit": limit, "ordering": ordering, "reverse": reverse}


async def validate_user_guid(user_service: UserServiceDep, guid: UUID4) -> User:
    user = await user_service.get_one(guid=guid)

    if not user:
        raise HTTPException(status_code=404, detail="Not found")

    return user
