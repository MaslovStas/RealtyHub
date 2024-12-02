from dataclasses import asdict

from httpx import AsyncClient

from src.fake_generators import RealtyFake, UserFake
from src.realty.models import Realty
from tests.integration.utils import (
    compare_realtys_in_out,
    compare_users_in_out,
    login,
    make_request_and_check_unauthorized,
)


async def test_success_current_user(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    fake_user_1: UserFake,
) -> None:
    """Тест на успешное получение данных текущего пользователя"""
    response = await client.get(
        url="/users/me/",
        headers=auth_access_headers_1,
    )
    assert response.status_code == 200
    compare_users_in_out(
        user_in=fake_user_1,
        user_out=response.json(),
        user_id=1,
    )


async def test_error_current_user_unauthorized(
    client: AsyncClient,
) -> None:
    """Тест на ошибку получения данных неавторизованного текущего пользователя"""
    await make_request_and_check_unauthorized(
        ac=client,
        method="get",
        url="/users/me/",
    )


async def test_error_current_user_with_refresh_token(
    client: AsyncClient,
    auth_refresh_headers_1: dict[str, str],
) -> None:
    """Тест на получение данных текущего авторизованного пользователя c помощью refresh
    токена"""
    await make_request_and_check_unauthorized(
        ac=client,
        method="get",
        url="/users/me/",
        headers=auth_refresh_headers_1,
    )


async def test_success_update_user(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    fake_user_update_1: UserFake,
) -> None:
    user_id = 1
    response = await client.patch(
        url=f"/users/{user_id}/",
        headers=auth_access_headers_1,
        json=asdict(fake_user_update_1),
    )
    assert response.status_code == 200

    compare_users_in_out(
        user_in=fake_user_update_1,
        user_out=response.json(),
        user_id=1,
    )
    response = await login(
        ac=client,
        email=fake_user_update_1.email,
        password=fake_user_update_1.password,
    )
    assert response.status_code == 200


async def test_error_update_email_already_existed(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    fake_user_2: UserFake,
) -> None:
    user_id = 1
    response = await client.patch(
        url=f"/users/{user_id}/",
        headers=auth_access_headers_1,
        json=asdict(fake_user_2),
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Email is already exists"


async def test_error_update_user_unauthorized(
    client: AsyncClient,
) -> None:
    """Тест на ошибку обновления данных неавторизованного пользователя"""
    user_id = 1
    await make_request_and_check_unauthorized(
        ac=client,
        method="patch",
        url=f"/users/{user_id}/",
    )


async def test_error_update_user_authorized_not_owner(
    client: AsyncClient,
    auth_access_headers_2: dict[str, str],
) -> None:
    """Тест на ошибку обновления данных неавторизованного пользователя"""
    user_id = 1
    await make_request_and_check_unauthorized(
        ac=client,
        method="patch",
        url=f"/users/{user_id}/",
        headers=auth_access_headers_2,
        expected_status_code=403,
    )


async def test_success_get_my_realtys(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    realtys: list[Realty],
    fake_realty_1: RealtyFake,
) -> None:
    """Тест на успешное получение объявлений текущего пользователя"""
    response = await client.get(
        url="/users/me/realtys",
        headers=auth_access_headers_1,
    )
    assert response.status_code == 200
    realtys_out = response.json()
    realtys_in = [
        fake_realty_1,
    ]
    for realty_in, realty_out in zip(realtys_in, realtys_out, strict=False):
        compare_realtys_in_out(
            realty_in=realty_in,
            realty_out=realty_out,
            is_full=False,
        )


async def test_error_get_my_realtys_unauthorized(
    client: AsyncClient,
) -> None:
    """Тест на ошибку получения объявлений неавторизованного пользователя"""
    await make_request_and_check_unauthorized(
        ac=client,
        method="get",
        url="/users/me/realtys",
    )
