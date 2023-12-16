from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.database.db import init_db
from src.auth.authviews import login_router
from src.user.userviews import user_router
from src.thread.threadviews import thread_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_db()
    yield


app = FastAPI(debug=False, title='FastAPIThreads', lifespan=lifespan)


main_api_router = APIRouter()

main_api_router.include_router(router=login_router, prefix='/auth', tags=['Auth'])
main_api_router.include_router(router=user_router, prefix='/users', tags=['Users'])
main_api_router.include_router(router=thread_router, prefix='/threads', tags=['Threads'])

app.include_router(main_api_router, prefix='/api')
