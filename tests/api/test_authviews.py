import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope='session')
async def test_create_token(client: AsyncClient) -> None:
    test_user_data = {'username': 'auth_username',
                      'email': 'auth_email@example.com',
                      'password': 'passwordpassword'}
    await client.post('/api/users', json=test_user_data)

    auth_form_data = {'username': 'auth_username', 'password': 'passwordpassword'}
    res = await client.post('/api/auth/create_token', data=auth_form_data)
    token = res.json()
    assert res.status_code == 201
    assert token
    assert token['access_token']
