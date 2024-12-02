from dataclasses import asdict

from httpx import AsyncClient

from src.auth.schemas import Token
from src.fake_generators import UserFake
from src.user.models import User
from tests.integration.utils import login, make_request_and_check_unauthorized


async def test_success_registration(
    client: AsyncClient,
    fake_user_1: UserFake,
) -> None:
    """Тест на успешную регистрацию незарегистрированного пользователя"""
    response = await client.post(
        url="/auth/jwt/register",
        json=asdict(fake_user_1),
    )
    assert response.status_code == 201
    token = Token(**response.json())
    assert token.token_type == "Bearer"


async def test_error_registration_email_already_exists(
    client: AsyncClient,
    users: list[User],
    fake_user_1: UserFake,
) -> None:
    """Тест на попытку зарегистрировать уже существующую почту"""
    response = await client.post(
        url="/auth/jwt/register",
        json=asdict(fake_user_1),
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Email is already exists"


async def test_success_login(
    client: AsyncClient,
    users: list[User],
    fake_user_1: UserFake,
) -> None:
    """Тест на успешный вход неавторизованного пользователя"""
    response = await login(
        ac=client,
        email=fake_user_1.email,
        password=fake_user_1.password,
    )
    assert response.status_code == 200
    token = Token(**response.json())
    assert token.token_type == "Bearer"


async def test_error_login(
    client: AsyncClient, users: list[User], fake_user_1: UserFake
) -> None:
    """Тест на ошибочный вход неавторизованного пользователя"""
    response = await login(
        ac=client,
        email=fake_user_1.email,
        password=fake_user_1.password[:-1],
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


async def test_success_reissue_token(
    client: AsyncClient, auth_refresh_headers_1: dict[str, str]
) -> None:
    """Тест на успешный перевыпуск токенов"""
    response = await client.post(
        url="/auth/jwt/refresh",
        headers=auth_refresh_headers_1,
    )
    assert response.status_code == 200
    token = Token(**response.json())
    assert token.token_type == "Bearer"


async def test_error_reissue_token_unauthorized(
    client: AsyncClient,
) -> None:
    """Тест на ошибочный перевыпуск токенов для неавторизованного пользователя"""
    await make_request_and_check_unauthorized(
        ac=client,
        method="post",
        url="/auth/jwt/refresh",
    )


async def test_error_reissue_token_with_access_token(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
) -> None:
    """Тест на ошибочный перевыпуск токенов для пользователя, авторизованного
    с помощью access токена"""
    await make_request_and_check_unauthorized(
        ac=client,
        method="post",
        url="/auth/jwt/refresh",
        headers=auth_access_headers_1,
    )
