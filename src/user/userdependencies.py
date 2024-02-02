from typing import Any, Annotated

from fastapi import HTTPException, Query, Depends
from beanie import PydanticObjectId

from src.user.usermodels import UserDB
from src.user.userschemas import UserGet
from src.user.userservice import UserService

UserServiceDep = Annotated[UserService, Depends()]


async def get_user_list_params(page: Annotated[int, Query(gt=0)] = 1,
                               limit: Annotated[int, Query(gt=0, le=10)] = 5,
                               ordering: Annotated[str, Query(enum=list(UserGet.model_fields))] = 'username',
                               reverse: bool = False) -> dict[str, Any]:
    return {'page': page,
            'limit': limit,
            'ordering': ordering,
            'reverse': reverse}


async def validate_user_id(user_service: UserServiceDep, user_id: PydanticObjectId) -> UserDB:
    user = await user_service.get_one(_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail='Not found')

    return user
