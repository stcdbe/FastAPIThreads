from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from src.core.database.mongo import get_thread_collection, get_user_collection
from src.main import app
from tests.mongo import clear_mongo_collections, get_test_thread_collection, get_test_user_collection

app.dependency_overrides[get_user_collection] = get_test_user_collection
app.dependency_overrides[get_thread_collection] = get_test_thread_collection


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_db() -> AsyncGenerator[None, None]:
    await clear_mongo_collections()
    yield
    await clear_mongo_collections()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as cli:
        yield cli


@pytest_asyncio.fixture(scope="session")
async def user_token_headers(client: AsyncClient) -> dict[str, str]:
    reg_data = {
        "username": "auth_username",
        "email": "auth_user@example.com",
        "password": "passwordpassword",
    }
    await client.post("/api/v1/users", json=reg_data)

    reg_data.pop("email")
    res = await client.post("api/v1/auth/create_token", data=reg_data)

    access_token = res.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest_asyncio.fixture(scope="session")
async def test_user_guid(client: AsyncClient) -> str:
    user_data = {
        "username": "username",
        "email": "user@example.com",
        "password": "passwordpassword",
    }
    res = await client.post("/api/v1/users", json=user_data)
    return res.json()["guid"]


@pytest_asyncio.fixture(scope="session")
async def test_thread_guid(client: AsyncClient, user_token_headers: dict[str, str]) -> str:
    thread_data = {"title": "test_title", "text": "test_text"}
    res = await client.post(
        "/api/v1/threads",
        json=thread_data,
        headers=user_token_headers,
    )
    return res.json()["guid"]
