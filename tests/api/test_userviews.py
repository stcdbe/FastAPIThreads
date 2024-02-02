import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope='session')
async def test_get_some_users(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    res = await client.get('/api/users', headers=user_token_headers)
    assert res.status_code == 200


@pytest.mark.asyncio(scope='session')
async def test_create_user(client: AsyncClient) -> None:
    test_user_data = {'username': 'test_username',
                      'email': 'test_email@example.com',
                      'password': 'passwordpassword'}

    res = await client.post('/api/users', json=test_user_data)
    created_user = res.json()
    assert res.status_code == 201
    assert created_user
    assert created_user.get('password') is None
    test_user_data.pop('password')
    for key, val in test_user_data.items():
        assert created_user[key] == val


@pytest.mark.asyncio(scope='session')
async def test_get_me(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    res = await client.get('/api/users/me', headers=user_token_headers)
    current_user = res.json()
    assert res.status_code == 200
    assert current_user


@pytest.mark.asyncio(scope='session')
async def test_patch_me(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    patch_user_data = {'username': 'patch_username',
                       'email': 'patch_email@example.com',
                       'password': 'passwordpassword'}
    res = await client.patch('/api/users/me',
                             json=patch_user_data,
                             headers=user_token_headers)
    upd_user = res.json()
    assert res.status_code == 200
    assert upd_user
    assert upd_user.get('password') is None
    patch_user_data.pop('password')
    for key, val in patch_user_data.items():
        assert upd_user[key] == val


@pytest.mark.asyncio(scope='session')
async def test_get_user(client: AsyncClient,
                        user_token_headers: dict[str, str],
                        test_user_id: str) -> None:
    res = await client.get(f'api/users/{test_user_id}', headers=user_token_headers)
    user = res.json()
    assert res.status_code == 200
    assert user
    assert user.get('id') == test_user_id
