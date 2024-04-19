import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope='session')
async def test_get_some_users(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    res = await client.get('/api/v1/users', headers=user_token_headers)
    assert res.status_code == 200


@pytest.mark.asyncio(scope='session')
async def test_create_user(client: AsyncClient) -> None:
    data = {'username': 'test_username',
            'email': 'test_email@example.com',
            'password': 'passwordpassword'}

    res = await client.post('/api/v1/users', json=data)
    user = res.json()
    assert res.status_code == 201
    assert user
    assert user.get('password') is None
    data.pop('password')
    for key, val in data.items():
        assert user[key] == val


@pytest.mark.asyncio(scope='session')
async def test_get_me(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    res = await client.get('/api/v1/users/me', headers=user_token_headers)
    user = res.json()
    assert res.status_code == 200
    assert user


@pytest.mark.asyncio(scope='session')
async def test_patch_me(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    data = {'username': 'patch_username',
            'email': 'patch_email@example.com',
            'password': 'passwordpassword'}

    res = await client.patch('/api/v1/users/me',
                             json=data,
                             headers=user_token_headers)
    user = res.json()
    assert res.status_code == 200
    assert user
    assert user.get('password') is None
    data.pop('password')
    for key, val in data.items():
        assert user[key] == val


@pytest.mark.asyncio(scope='session')
async def test_get_user(client: AsyncClient,
                        user_token_headers: dict[str, str],
                        test_user_guid: str) -> None:
    res = await client.get(f'api/v1/users/{test_user_guid}', headers=user_token_headers)
    user = res.json()
    assert res.status_code == 200
    assert user
    assert user['guid'] == test_user_guid
