from typing import Annotated, Any

from fastapi import APIRouter, Depends

from src.auth.auth_dependencies import CurrentUserDep
from src.thread.thread_dependencies import (get_thread_list_params,
                                            validate_thread_id,
                                            ThreadServiceDep,
                                            validate_thread_is_active, CommentServiceDep, validate_thread_perms)
from src.thread.thread_models import ThreadDB
from src.thread.thread_schemas import CommentCreate, ThreadCreate, ThreadGet, ThreadWithCommentsGet

thread_router = APIRouter(prefix='/threads', tags=['Threads'])


@thread_router.get(path='',
                   status_code=200,
                   response_model=list[ThreadGet],
                   name='Get some threads')
async def get_some_threads(current_user: CurrentUserDep,
                           thread_service: ThreadServiceDep,
                           params: Annotated[dict[str, Any], Depends(get_thread_list_params)]) -> list[ThreadDB]:
    return await thread_service.get_list(params=params)


@thread_router.post(path='',
                    status_code=201,
                    response_model=ThreadGet,
                    name='Crete a new thread')
async def create_thread(current_user: CurrentUserDep,
                        thread_service: ThreadServiceDep,
                        thread_data: ThreadCreate) -> Any:
    return await thread_service.create_one(thread_data=thread_data)


@thread_router.get(path='/{thread_id}',
                   status_code=200,
                   response_model=ThreadWithCommentsGet,
                   name='Get the thread by id')
async def get_thread(current_user: CurrentUserDep,
                     thread: Annotated[ThreadDB, Depends(validate_thread_id)]) -> ThreadDB:
    return thread


@thread_router.post(path='/{thread_id}',
                    status_code=201,
                    response_model=ThreadWithCommentsGet,
                    name='Create a new thread comment')
async def create_thread_com(current_user: CurrentUserDep,
                            comment_service: CommentServiceDep,
                            thread: Annotated[ThreadDB, Depends(validate_thread_is_active)],
                            com_data: CommentCreate) -> ThreadDB:
    return await comment_service.create_one(thread=thread, com_data=com_data)


@thread_router.delete(path='/{thread_id}',
                      status_code=204,
                      name='Delete the thread by id')
async def del_thread(thread_service: ThreadServiceDep,
                     thread: Annotated[ThreadDB, Depends(validate_thread_perms)]) -> None:
    await thread_service.del_one(thread=thread)
