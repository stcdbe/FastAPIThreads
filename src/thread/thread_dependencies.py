from typing import Any, Annotated

from beanie import PydanticObjectId
from fastapi import HTTPException, Query, Depends

from src.auth.auth_dependencies import CurrentUserDep
from src.thread.thread_models import ThreadDB
from src.thread.thread_schemas import ThreadGet
from src.thread.thread_services import ThreadService, CommentService
from src.user.user_enums import UserStatus

ThreadServiceDep = Annotated[ThreadService, Depends()]
CommentServiceDep = Annotated[CommentService, Depends()]


async def get_thread_list_params(page: Annotated[int, Query(gt=0)] = 1,
                                 limit: Annotated[int, Query(gt=0, le=10)] = 5,
                                 ordering: Annotated[str, Query(enum=list(ThreadGet.model_fields))] = 'title',
                                 reverse: bool = False) -> dict[str, Any]:
    return {'page': page,
            'limit': limit,
            'ordering': ordering,
            'reverse': reverse}


async def validate_thread_id(thread_service: ThreadServiceDep, thread_id: PydanticObjectId) -> ThreadDB:
    thread = await thread_service.get_one(_id=thread_id)

    if not thread:
        raise HTTPException(status_code=404, detail='Not found')

    return thread


async def validate_thread_is_active(thread: Annotated[ThreadDB, Depends(validate_thread_id)]) -> ThreadDB:
    if not thread.is_active:
        raise HTTPException(status_code=409, detail='Thread is closed')

    return thread


async def validate_thread_perms(thread: Annotated[ThreadDB, Depends(validate_thread_id)],
                                current_user: CurrentUserDep) -> ThreadDB:
    if current_user.status != UserStatus.admin:
        raise HTTPException(status_code=403, detail='Forbidden request')

    return thread
