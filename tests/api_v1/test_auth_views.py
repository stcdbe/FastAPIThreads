import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope='session')
async def test_create_token(client: AsyncClient) -> None:
    data = {'username': 'new_auth_username',
            'email': 'new_auth_email@example.com',
            'password': 'passwordpassword'}
    await client.post('/api/v1/users', json=data)

    form_data = {'username': 'new_auth_username', 'password': 'passwordpassword'}
    res = await client.post('/api/v1/auth/create_token', data=form_data)
    token = res.json()
    assert res.status_code == 201
    assert token
    assert token['access_token']
