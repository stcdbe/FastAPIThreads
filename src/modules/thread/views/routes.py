from typing import Annotated, Any

from fastapi import APIRouter, Depends

from src.modules.auth.dependencies import CurrentUserAdminDep, CurrentUserDep
from src.modules.thread.dependencies import (
    CommentServiceDep,
    ThreadServiceDep,
    check_thread_is_active,
    get_thread_list_params,
    validate_thread_guid,
)
from src.modules.thread.models.entities import Thread
from src.modules.thread.views.schemas import CommentCreate, ThreadCreate, ThreadGet, ThreadWithCommentsGet

thread_router = APIRouter(prefix="/threads", tags=["Threads"])


@thread_router.get(
    path="",
    status_code=200,
    response_model=list[ThreadGet],
    name="Get some threads",
)
async def get_some_threads(
    _: CurrentUserDep,
    thread_service: ThreadServiceDep,
    params: Annotated[dict[str, Any], Depends(get_thread_list_params)],
) -> list[Thread]:
    return await thread_service.get_list(params=params)


@thread_router.post(
    path="",
    status_code=201,
    response_model=ThreadGet,
    name="Create a new thread",
)
async def create_thread(
    _: CurrentUserDep,
    thread_service: ThreadServiceDep,
    thread_data: ThreadCreate,
) -> Thread:
    return await thread_service.create_one(thread_data=thread_data)


@thread_router.get(
    path="/{guid}",
    status_code=200,
    response_model=ThreadWithCommentsGet,
    name="Get the thread by id",
)
async def get_thread(
    _: CurrentUserDep,
    thread: Annotated[Thread, Depends(validate_thread_guid)],
) -> Thread:
    return thread


@thread_router.post(
    path="/{guid}",
    status_code=201,
    response_model=ThreadWithCommentsGet,
    name="Create a new thread comment",
)
async def create_thread_com(
    _: CurrentUserDep,
    comment_service: CommentServiceDep,
    thread: Annotated[Thread, Depends(check_thread_is_active)],
    data: CommentCreate,
) -> Thread:
    return await comment_service.create_one(thread=thread, data=data)


@thread_router.delete(
    path="/{guid}",
    status_code=204,
    name="Delete the thread by id",
)
async def delete_thread(
    _: CurrentUserAdminDep,
    thread_service: ThreadServiceDep,
    thread: Annotated[Thread, Depends(validate_thread_guid)],
) -> None:
    await thread_service.delete_one(thread=thread)
