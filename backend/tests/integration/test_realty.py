from dataclasses import asdict

import pytest
from httpx import AsyncClient

from src.fake_generators import RealtyFake
from src.realty.models import Realty, RealtyType
from tests.integration.utils import (
    compare_ids_favorites_realtys_in_out,
    compare_realtys_in_out,
)


async def test_success_get_realtys_unauthorized(
    client: AsyncClient,
    realtys: list[Realty],
    fake_realtys: list[RealtyFake],
) -> None:
    """Тест на получение объявлений"""
    active_fake_realtys = [realty for realty in fake_realtys if realty.is_active]

    response = await client.get(url="/realtys/")

    assert response.status_code == 200
    assert int(response.headers.get("x-total-count")) == len(active_fake_realtys)

    realtys_out = response.json()
    assert len(realtys_out) == len(active_fake_realtys)

    # Проверяем сходство объявлений
    for realty_in, realty_out in zip(active_fake_realtys, realtys_out, strict=False):
        compare_realtys_in_out(
            realty_in=realty_in,
            realty_out=realty_out,
            is_full=False,
        )


async def test_success_get_realtys_authorized(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    realtys: list[Realty],
    favorites_realtys: list[Realty],
    fake_realtys: list[RealtyFake],
) -> None:
    """Тест на получение объявлений"""
    is_favorites = [
        realty in favorites_realtys for realty in realtys if realty.is_active
    ]
    active_fake_realtys = [realty for realty in fake_realtys if realty.is_active]

    response = await client.get(
        url="/realtys/",
        headers=auth_access_headers_1,
    )

    assert response.status_code == 200
    assert int(response.headers.get("x-total-count")) == len(active_fake_realtys)

    realtys_out = response.json()
    assert len(realtys_out) == len(active_fake_realtys)

    for is_favorite, realty_out in zip(is_favorites, realtys_out, strict=False):
        assert is_favorite == realty_out["is_favorite"]


@pytest.mark.parametrize(
    "params, expected_ids, expected_total",
    [
        ({"is_active": False}, [1, 2, 3, 4, 5, 6], 6),
        ({"limit": 2, "offset": 2, "order_by": "price", "desc_order": True}, [2, 1], 5),
        ({"min_price": 1100, "max_price": 1900, "order_by": "price"}, [2, 1, 3], 3),
        ({"city": "LANd", "order_by": "price", "desc_order": True}, [2, 1, 3], 3),
        (
            {"with_photos": True, "order_by": "price", "type": RealtyType.APARTMENT},
            [2, 1],
            2,
        ),
    ],
)
async def test_search_realtys(
    client: AsyncClient,
    realtys: list[Realty],
    params: dict[str, int | str | bool],
    expected_ids: list[int],
    expected_total: int,
) -> None:
    """Тест на поисковый фильтр для объявлений"""
    response = await client.get(url="/realtys/", params=params)
    realtys_out_ids = [realty_out["id"] for realty_out in response.json()]

    assert response.status_code == 200
    assert realtys_out_ids == expected_ids
    assert int(response.headers.get("x-total-count")) == expected_total


async def test_success_get_realty(
    client: AsyncClient,
    realtys: list[Realty],
    fake_realty_1: RealtyFake,
) -> None:
    """Тест на получение объявления"""
    realty_id = 1
    response = await client.get(url=f"/realtys/{realty_id}/")
    assert response.status_code == 200
    # Проверяем сходство данных объявления
    compare_realtys_in_out(realty_in=fake_realty_1, realty_out=response.json())


async def test_error_get_realty(
    client: AsyncClient,
    realtys: list[Realty],
) -> None:
    """Тест на получение несуществующего объявления"""
    realty_id = len(realtys) + 1
    response = await client.get(url=f"/realtys/{realty_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Realty id={realty_id} not found"


async def test_success_create_realty(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    fake_realty_1: RealtyFake,
) -> None:
    """Тест на успешное создание нового объявления"""
    response = await client.post(
        url="/realtys/",
        json=asdict(fake_realty_1),
        headers=auth_access_headers_1,
    )
    assert response.status_code == 201
    compare_realtys_in_out(realty_in=fake_realty_1, realty_out=response.json())


async def test_success_update_realty(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    realtys: list[Realty],
    fake_realty_update_1: RealtyFake,
) -> None:
    """Тест на успешное обновление объявления"""
    realty_id = 1
    response = await client.patch(
        url=f"/realtys/{realty_id}/",
        json=asdict(fake_realty_update_1),
        headers=auth_access_headers_1,
    )
    assert response.status_code == 200

    compare_realtys_in_out(
        realty_in=fake_realty_update_1,
        realty_out=response.json(),
        is_update=True,
    )


async def test_success_delete_realty(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    realtys: list[Realty],
) -> None:
    """Тест на успешное удаление объявления"""
    realty_id = 1
    response = await client.delete(
        url=f"/realtys/{realty_id}/",
        headers=auth_access_headers_1,
    )
    assert response.status_code == 204

    response = await client.get(
        url=f"/realtys/{realty_id}/",
        headers=auth_access_headers_1,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"Realty id={realty_id} not found"


@pytest.mark.parametrize(
    "url, method",
    [
        ("/realtys/1/", "patch"),
        ("/realtys/1/", "delete"),
    ],
)
async def test_error_realty_authorized_not_owner(
    client: AsyncClient,
    auth_access_headers_2: dict[str, str],
    realtys: list[Realty],
    url: str,
    method: str,
) -> None:
    """Тест на неудачное действие с объявлением не владельцем"""
    request = getattr(client, method)
    response = await request(
        url=url,
        headers=auth_access_headers_2,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"


async def test_success_get_favorites_realtys(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    favorites_realtys: list[Realty],
) -> None:
    """Тест на успешное получение избранных объявлений"""
    response = await client.get(
        url="/realtys/favorites",
        headers=auth_access_headers_1,
    )
    assert response.status_code == 200
    assert (int(response.headers.get("x-total-count"))) == len(favorites_realtys)
    compare_ids_favorites_realtys_in_out(
        favorites_in=favorites_realtys,
        favorites_out=response.json(),
    )


async def test_success_add_favorite_realty(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    realtys: list[Realty],
    favorites_realtys: list[Realty],
) -> None:
    """Тест на успешное добавление последнего объявления в избранное"""
    realty_id = realtys[-1].id
    response = await client.post(
        url=f"/realtys/favorites/{realty_id}/",
        headers=auth_access_headers_1,
    )
    added_realty: Realty = realtys[-1]
    assert response.status_code == 201

    response = await client.get(
        url="/realtys/favorites",
        headers=auth_access_headers_1,
    )
    assert response.status_code == 200
    assert (int(response.headers.get("x-total-count"))) == len(favorites_realtys) + 1

    compare_ids_favorites_realtys_in_out(
        favorites_in=favorites_realtys + [added_realty],
        favorites_out=response.json(),
    )


async def test_success_delete_favorite_realty(
    client: AsyncClient,
    auth_access_headers_1: dict[str, str],
    favorites_realtys: list[Realty],
) -> None:
    """Тест на успешное удаление последнего избранного объявления"""
    realty_id = favorites_realtys[-1].id
    response = await client.delete(
        url=f"/realtys/favorites/{realty_id}/",
        headers=auth_access_headers_1,
    )
    assert response.status_code == 204

    response = await client.get(
        url="/realtys/favorites",
        headers=auth_access_headers_1,
    )
    assert response.status_code == 200
    assert (int(response.headers.get("x-total-count"))) == len(favorites_realtys) - 1

    compare_ids_favorites_realtys_in_out(
        favorites_in=favorites_realtys[:-1],
        favorites_out=response.json(),
    )


@pytest.mark.parametrize(
    "url, method",
    [
        ("/realtys/favorites", "get"),
        ("/realtys/favorites/1/", "post"),
        ("/realtys/favorites/1/", "delete"),
        ("/realtys/", "post"),
        ("/realtys/1/", "patch"),
        ("/realtys/1/", "delete"),
    ],
)
async def test_error_realty_unauthorized(
    client: AsyncClient,
    realtys: list[Realty],
    url: str,
    method: str,
) -> None:
    """Тест на запрет действий для неавторизованного пользователя"""
    request = getattr(client, method)
    response = await request(url=url)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
