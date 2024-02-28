from typing import Any, AsyncGenerator

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import pytest_asyncio
from httpx import AsyncClient

from src.config import settings
from src.main import app
from src.user.user_models import UserDB
from src.thread.thread_models import ThreadDB

mongo_client = AsyncIOMotorClient(settings.MONGO_URL_TEST)
db = mongo_client[settings.MONGO_DB_TEST]


async def clean_test_db() -> None:
    for collection in await db.list_collection_names():
        await db[collection].drop()


async def init_test_db() -> None:
    await init_beanie(database=db, document_models=[UserDB, ThreadDB])


@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_db() -> AsyncGenerator[Any, None]:
    await clean_test_db()
    await init_test_db()
    yield
    await clean_test_db()


@pytest_asyncio.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as cli:
        yield cli


@pytest_asyncio.fixture(scope='session')
async def user_token_headers(client: AsyncClient) -> dict[str, str]:
    reg_data = {'username': 'auth_username',
                'email': 'auth_user@example.com',
                'password': 'passwordpassword'}
    await client.post('/api/users', json=reg_data)

    reg_data.pop('email')
    res = await client.post('api/auth/create_token', data=reg_data)

    access_token = res.json()['access_token']
    return {'Authorization': f'Bearer {access_token}'}


@pytest_asyncio.fixture(scope='session')
async def test_user_id(client: AsyncClient) -> str:
    user_data = {'username': 'username',
                 'email': 'user@example.com',
                 'password': 'passwordpassword'}
    res = await client.post('/api/users', json=user_data)
    return res.json()['id']


@pytest_asyncio.fixture(scope='session')
async def test_thread_id(client: AsyncClient, user_token_headers: dict[str, str]) -> str:
    thread_data = {'title': 'test_title', 'text': 'test_text'}
    res = await client.post('/api/threads',
                            json=thread_data,
                            headers=user_token_headers)
    return res.json()['id']
