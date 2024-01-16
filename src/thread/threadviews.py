from typing import Annotated, Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from src.database.dbmodels import UserDB
from src.thread.threadschemas import CommentCreate, ThreadCreate, ThreadGet, ThredWithCommentsGet
from src.thread.threadservice import (create_com_db,
                                      create_thread_db,
                                      del_thread_db,
                                      get_some_threads_db,
                                      get_thread_db)
from src.auth.authutils import get_current_user


thread_router = APIRouter()


@thread_router.get('',
                   status_code=200,
                   response_model=list[ThreadGet],
                   name='Get some threads')
async def get_some_threads(current_user: Annotated[UserDB, Depends(get_current_user)],
                           page: Annotated[int, Query(gt=0)] = 1,
                           limit: Annotated[int, Query(gt=0, le=10)] = 5,
                           ordering: Annotated[str, Query(enum=list(ThreadGet.model_fields))] = 'title',
                           reverse: bool = False) -> Any:
    offset = (page - 1) * limit
    return await get_some_threads_db(offset=offset,
                                     limit=limit,
                                     ordering=ordering,
                                     reverse=reverse)


@thread_router.post('',
                    status_code=201,
                    response_model=ThreadGet,
                    name='Crete a new thread')
async def create_thread(current_user: Annotated[UserDB, Depends(get_current_user)],
                        thread_data: ThreadCreate) -> Any:
    return await create_thread_db(thread_data=thread_data, creator=current_user)


@thread_router.get('/{thread_id}',
                   status_code=200,
                   response_model=ThredWithCommentsGet,
                   name='Get the thread by id')
async def get_thread(current_user: Annotated[UserDB, Depends(get_current_user)],
                     thread_id: PydanticObjectId) -> Any:
    thread = await get_thread_db(thread_id=thread_id)

    if not thread:
        raise HTTPException(status_code=404, detail='Not found')

    return thread


@thread_router.post('/{thread_id}',
                    status_code=201,
                    response_model=ThredWithCommentsGet,
                    name='Create a new thread comment')
async def create_thread_com(current_user: Annotated[UserDB, Depends(get_current_user)],
                            thread_id: PydanticObjectId,
                            com_data: CommentCreate) -> Any:
    thread = await get_thread_db(thread_id=thread_id)

    if not thread:
        raise HTTPException(status_code=404, detail='Not found')

    if not thread.is_active:
        raise HTTPException(status_code=409, detail='Thread is closed')

    return await create_com_db(com_data=com_data, thread=thread)


@thread_router.delete('/{thread_id}',
                      status_code=204,
                      name='Delete the thread by id')
async def del_thread(current_user: Annotated[UserDB, Depends(get_current_user)],
                     thread_id: PydanticObjectId) -> None:
    thread = await get_thread_db(thread_id=thread_id)

    if not thread:
        raise HTTPException(status_code=404, detail='Not found')

    if current_user.id != thread.creator.id:
        raise HTTPException(status_code=403, detail='Forbidden request')

    await del_thread_db(thread=thread)
