import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope='session')
async def test_get_some_threads(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    res = await client.get('/api/v1/threads', headers=user_token_headers)
    assert res.status_code == 200


@pytest.mark.asyncio(scope='session')
async def test_create_thread(client: AsyncClient, user_token_headers: dict[str, str]) -> None:
    data = {'title': 'test_title', 'text': 'test_text'}
    res = await client.post('/api/v1/threads',
                            json=data,
                            headers=user_token_headers)
    created_thread = res.json()
    assert res.status_code == 201
    assert created_thread
    for key, val in data.items():
        assert created_thread[key] == val


@pytest.mark.asyncio(scope='session')
async def test_get_thread(client: AsyncClient,
                          user_token_headers: dict[str, str],
                          test_thread_guid: str) -> None:
    res = await client.get(f'/api/v1/threads/{test_thread_guid}', headers=user_token_headers)
    thread = res.json()
    assert res.status_code == 200
    assert thread
    assert thread['guid'] == test_thread_guid


@pytest.mark.asyncio(scope='session')
async def test_create_thread_com(client: AsyncClient,
                                 test_thread_guid: str,
                                 user_token_headers: dict[str, str]) -> None:
    com_data = {'text': 'comment_text'}
    res = await client.post(f'/api/v1/threads/{test_thread_guid}',
                            json=com_data,
                            headers=user_token_headers)
    thread = res.json()
    assert res.status_code == 201
    assert thread
    assert com_data['text'] in {comment['text'] for comment in thread['comments']}


@pytest.mark.asyncio(scope='session')
async def test_del_thread(client: AsyncClient,
                          test_thread_guid: str,
                          user_token_headers: dict[str, str]) -> None:
    res = await client.delete(f'/api/v1/threads/{test_thread_guid}', headers=user_token_headers)
    assert res.status_code == 403
