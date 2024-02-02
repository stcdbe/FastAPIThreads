from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from src.auth.authdependencies import CurrentUserDep
from src.thread.threaddependencies import get_thread_list_params, validate_thread_id, ThreadServiceDep
from src.thread.threadmodels import ThreadDB
from src.thread.threadschemas import CommentCreate, ThreadCreate, ThreadGet, ThreadWithCommentsGet
from src.user.userenums import UserStatus

thread_router = APIRouter()


@thread_router.get('',
                   status_code=200,
                   response_model=list[ThreadGet],
                   name='Get some threads')
async def get_some_threads(current_user: CurrentUserDep,
                           thread_service: ThreadServiceDep,
                           params: Annotated[dict[str, Any], Depends(get_thread_list_params)]) -> list[ThreadDB]:
    return await thread_service.get_list(params=params)


@thread_router.post('',
                    status_code=201,
                    response_model=ThreadGet,
                    name='Crete a new thread')
async def create_thread(current_user: CurrentUserDep,
                        thread_service: ThreadServiceDep,
                        thread_data: ThreadCreate) -> Any:
    return await thread_service.create_one(thread_data=thread_data)


@thread_router.get('/{thread_id}',
                   status_code=200,
                   response_model=ThreadWithCommentsGet,
                   name='Get the thread by id')
async def get_thread(current_user: CurrentUserDep,
                     thread: Annotated[ThreadDB, Depends(validate_thread_id)]) -> ThreadDB:
    return thread


@thread_router.post('/{thread_id}',
                    status_code=201,
                    response_model=ThreadWithCommentsGet,
                    name='Create a new thread comment')
async def create_thread_com(current_user: CurrentUserDep,
                            thread_service: ThreadServiceDep,
                            thread: Annotated[ThreadDB, Depends(validate_thread_id)],
                            com_data: CommentCreate) -> ThreadDB:
    if not thread.is_active:
        raise HTTPException(status_code=409, detail='Thread is closed')

    return await thread_service.create_com(thread=thread, com_data=com_data)


@thread_router.delete('/{thread_id}',
                      status_code=204,
                      name='Delete the thread by id')
async def del_thread(current_user: CurrentUserDep,
                     thread_service: ThreadServiceDep,
                     thread: Annotated[ThreadDB, Depends(validate_thread_id)]) -> None:
    if current_user.status != UserStatus.admin:
        raise HTTPException(status_code=403, detail='Forbidden request')

    await thread_service.del_one(thread=thread)
