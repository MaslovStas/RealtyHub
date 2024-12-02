from dataclasses import asdict
from typing import Any, Literal

from httpx import AsyncClient, Response

from src.fake_generators import ImageFake, RealtyFake, UserFake
from src.realty.models import Realty, RealtyType


async def login(
    ac: AsyncClient,
    email: str,
    password: str,
) -> Response:
    response = await ac.post(
        url="/auth/jwt/token",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response


async def auth_headers(
    ac: AsyncClient,
    fake_user: UserFake,
    type_token: Literal["access_token", "refresh_token"],
) -> dict[str, str]:
    response = await login(
        ac,
        fake_user.email,
        fake_user.password,
    )
    token = response.json()[type_token]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


async def make_request_and_check_unauthorized(
    ac: AsyncClient,
    method: Literal["get", "post", "patch", "delete"],
    url: str,
    headers: dict[str, str] | None = None,
    expected_status_code: Literal[401, 403] = 401,
) -> None:
    details = {401: "Not authenticated", 403: "Permission denied"}
    request = getattr(ac, method)
    response = await request(url=url, headers=headers)
    assert response.status_code == expected_status_code
    assert response.json()["detail"] == details[expected_status_code]


def compare_users_in_out(
    user_in: UserFake, user_out: dict[str, Any], user_id: int | None = None
) -> None:
    if user_id is not None:
        assert user_out.get("id") == user_id

    for name, value in asdict(user_in).items():
        if name != "password":
            assert user_out.get(name) == value


def compare_realtys_in_out(
    realty_in: RealtyFake,
    realty_out: dict[str, Any],
    is_update: bool = False,
    is_full: bool = True,
) -> None:
    """Проверка на идентичность входных фейковых данных и полученных данных с запроса"""
    # Проверяем сходство объявлений, кроме фото
    exclude = {"images"}
    if realty_in.type != RealtyType.APARTMENT:
        exclude.update({"floor", "rooms"})

    if is_update:
        exclude.add("type")

    for name, value in asdict(realty_in).items():
        if name not in exclude:
            assert realty_out.get(name) == value
    # Проверяем сходство фото
    images_in: list[ImageFake] = realty_in.images
    images_out: list[dict[str, str]]
    if is_full:
        images_out = realty_out["images"]
        assert len(images_in) == len(images_out)
    else:
        images_out = [realty_out["title_image"]]

    for image_in, image_out in zip(images_in, images_out, strict=False):
        for name, value in asdict(image_in).items():
            if not (name == "id" and value is None):
                assert image_out.get(name) == value


def compare_ids_favorites_realtys_in_out(
    favorites_in: list[Realty], favorites_out: list[dict[str, Any]]
) -> None:
    """Проверка на идентичность id`s добавленных объявлений и полученных данных
    с запроса"""
    assert len(favorites_out) == len(favorites_in)
    for favorite_in, favorite_out in zip(
        favorites_in,
        favorites_out,
        strict=False,
    ):
        assert favorite_in.id == favorite_out["id"]
