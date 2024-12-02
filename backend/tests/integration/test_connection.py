import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_connection(client: AsyncClient) -> None:
    response = await client.get(url="/healthcheck")
    assert response.status_code == 200
