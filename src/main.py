from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.auth.auth_views import login_router
from src.db import init_db
from src.thread.thread_views import thread_router
from src.user.user_views import user_router
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_db()
    yield


app = FastAPI(debug=settings.DEBUG,
              version='0.1.4',
              title='FastAPIThreads',
              lifespan=lifespan,
              docs_url=settings.DOCS_URL,
              redoc_url=settings.REDOC_URL)

main_api_router = APIRouter(prefix='/api')

main_api_router.include_router(router=login_router)
main_api_router.include_router(router=user_router)
main_api_router.include_router(router=thread_router)

app.include_router(main_api_router)
