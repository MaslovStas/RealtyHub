from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.fake_generators import UserFake
from src.main import app
from src.user.models import User
from tests.integration.utils import auth_headers


@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    def get_session_override() -> AsyncSession:
        return session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"accept": "application/json", "Content-Type": "application/json"},
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def auth_access_headers_1(
    client: AsyncClient,
    users: list[User],
    fake_user_1: UserFake,
) -> dict[str, str]:
    return await auth_headers(
        client,
        fake_user_1,
        type_token="access_token",
    )


@pytest.fixture
async def auth_access_headers_2(
    client: AsyncClient,
    users: list[User],
    fake_user_2: UserFake,
) -> dict[str, str]:
    return await auth_headers(
        client,
        fake_user_2,
        type_token="access_token",
    )


@pytest.fixture
async def auth_refresh_headers_1(
    client: AsyncClient, users: list[User], fake_user_1: UserFake
) -> dict[str, str]:
    return await auth_headers(
        client,
        fake_user_1,
        type_token="refresh_token",
    )
