from typing import Annotated, Any

from fastapi import Depends, HTTPException, Query
from pydantic import UUID4

from src.modules.thread.models.entities import Thread
from src.modules.thread.services.comment import CommentService
from src.modules.thread.services.thread import ThreadService
from src.modules.thread.views.schemas import ThreadGet

ThreadServiceDep = Annotated[ThreadService, Depends()]
CommentServiceDep = Annotated[CommentService, Depends()]


async def get_thread_list_params(
    offset: Annotated[int, Query(ge=0, le=10)] = 0,
    limit: Annotated[int, Query(gt=0, le=10)] = 5,
    ordering: Annotated[str, Query(enum=tuple(ThreadGet.model_fields))] = "title",
    reverse: bool = False,
) -> dict[str, Any]:
    return {"offset": offset, "limit": limit, "ordering": ordering, "reverse": reverse}


async def validate_thread_guid(thread_service: ThreadServiceDep, guid: UUID4) -> Thread:
    thread = await thread_service.get_one(guid=guid)

    if not thread:
        raise HTTPException(status_code=404, detail="Not found")

    return thread


async def check_thread_is_active(thread: Annotated[Thread, Depends(validate_thread_guid)]) -> Thread:
    if not thread.is_active:
        raise HTTPException(status_code=409, detail="Thread is closed")

    return thread
