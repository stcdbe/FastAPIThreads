import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope="session")
async def test_healthcheck(client: AsyncClient) -> None:
    res = await client.get("/ping")
    mes = res.json()
    assert res.status_code == 200
    assert mes
    assert mes["message"]
