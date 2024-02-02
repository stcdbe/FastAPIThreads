from typing import Any, Annotated

from beanie import PydanticObjectId
from fastapi import HTTPException, Query, Depends

from src.thread.threadmodels import ThreadDB
from src.thread.threadschemas import ThreadGet
from src.thread.threadservice import ThreadService

ThreadServiceDep = Annotated[ThreadService, Depends()]


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
