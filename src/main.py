from http import HTTPStatus

from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.config import settings
from src.core.presentation.schemas import Message
from src.modules.auth.views.routes import auth_router
from src.modules.thread.views.routes import thread_router
from src.modules.user.views.routes import user_router

app = FastAPI(
    debug=settings.DEBUG,
    version="0.2.1",
    title="FastAPIThreads",
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
)

api_v1_router = APIRouter(prefix="/api/v1")

for router in (user_router, auth_router, thread_router):
    api_v1_router.include_router(router=router)

app.include_router(router=api_v1_router)


@app.get(
    path="/ping",
    status_code=HTTPStatus.OK,
    response_model=Message,
    name="Healthcheck",
)
async def healthcheck() -> dict[str, str]:
    return {"message": "pong"}
