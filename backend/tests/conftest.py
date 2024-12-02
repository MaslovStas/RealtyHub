from collections.abc import AsyncGenerator
from dataclasses import asdict

import pytest
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.core.database import Base
from src.fake_generators import ImageFake, RealtyFake, UserFake
from src.realty.crud import realty_crud
from src.realty.models import Realty, RealtyType, UserRealtyFavorite
from src.realty.schemas import RealtySchemaCreate
from src.user.crud import user_crud
from src.user.models import User
from src.user.schemas import UserSchemaCreate


@pytest.fixture(name="session")
async def session_fixture() -> AsyncGenerator[AsyncSession, None]:
    assert settings.ENVIRONMENT.is_testing

    test_engine = create_async_engine(
        settings.db.DATABASE_URL,
        poolclass=StaticPool,
    )

    test_session_factory = async_sessionmaker(
        bind=test_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_factory() as session:
        yield session


# Создание фейковых пользователей
@pytest.fixture(scope="session")
def fake_user_1() -> UserFake:
    """Создание фейковых данных первого пользователя с заданными почтой и паролем"""
    return UserFake(email="mail@gmail.com")


@pytest.fixture(scope="session")
def fake_user_update_1() -> UserFake:
    """Создание фейковых данных для обновления первого пользователя со случайными
    почтой и паролем"""
    return UserFake(email="mail1@gmail.com")


@pytest.fixture(scope="session")
def fake_user_2() -> UserFake:
    """Создание фейковых данных второго пользователя со случайными данными"""
    return UserFake(email="mail2@gmail.com")


@pytest.fixture(scope="session")
def fake_users(fake_user_1: UserFake, fake_user_2: UserFake) -> list[UserFake]:
    """Возврат всех фейковых пользователей"""
    return [fake_user_1, fake_user_2] + [
        UserFake(email=f"mail{i + 3}@gmail.com") for i in range(4)
    ]


# Создание фейковых фото для первого объявления
@pytest.fixture(scope="session")
def fake_images(number_images: int = 3) -> list[ImageFake]:
    """Создание фейковых данных о фото для объявлений"""
    return [ImageFake() for _ in range(number_images)]


@pytest.fixture(scope="session")
def fake_images_changed(
    fake_images: list[ImageFake],
) -> list[ImageFake]:
    """Создание фейковых данных для обновления фото для объявлений, где меняются местами
    первый и последний элементы, так же удаляются и добавляются новые элементы"""
    first_photo, *_, last_photo = fake_images
    new_photo = ImageFake()
    first_photo.id = 1
    last_photo.id = 3
    return [last_photo, new_photo, first_photo]


# Создание фейковых объявлений
@pytest.fixture(scope="session")
def fake_realty_1(fake_images: list[ImageFake]) -> RealtyFake:
    """Создание фейковых данных активного объявления недвижимости"""
    return RealtyFake(
        price=1500,
        rooms=2,
        city="Nederland",
        type=RealtyType.APARTMENT,
        is_active=True,
        images=fake_images,
    )


@pytest.fixture(scope="session")
def fake_realty_update_1(
    fake_images_changed: list[ImageFake],
) -> RealtyFake:
    """Создание фейковых данных неактивного объявления недвижимости с изменёнными
    фото"""
    return RealtyFake(is_active=False, images=fake_images_changed)


@pytest.fixture(scope="session")
def fake_realtys(fake_realty_1: RealtyFake) -> list[RealtyFake]:
    """Возврат всех фейковых объявлений"""
    fake_realty_2 = RealtyFake(
        price=1700,
        rooms=3,
        city="Chicago Land",
        type=RealtyType.APARTMENT,
        is_active=True,
        number_images=3,
    )
    fake_realty_3 = RealtyFake(
        price=1200,
        city="Land",
        type=RealtyType.HOUSE,
        is_active=True,
        number_images=4,
    )
    fake_realty_4 = RealtyFake(
        price=1000,
        city="Landfall",
        type=RealtyType.COMMERCIAL,
        is_active=False,
        number_images=1,
    )
    fake_realty_5 = RealtyFake(
        price=2000,
        city="New York",
        type=RealtyType.APARTMENT,
        is_active=True,
        number_images=0,
    )
    fake_realty_6 = RealtyFake(
        price=5000,
        city="Kyiv",
        type=RealtyType.HOUSE,
        is_active=True,
        number_images=2,
    )
    return [
        fake_realty_1,
        fake_realty_2,
        fake_realty_3,
        fake_realty_4,
        fake_realty_5,
        fake_realty_6,
    ]


# Создание записей с пользователями и объявлениями в БД
@pytest.fixture
async def users(session: AsyncSession, fake_users: list[UserFake]) -> list[User]:
    """Создание в БД пользователей по фейковым данным"""
    users_in = [UserSchemaCreate(**asdict(fake_user)) for fake_user in fake_users]
    new_users = await user_crud.create_many(session, users_in)

    return new_users


@pytest.fixture
async def realtys(
    session: AsyncSession,
    users: list[User],
    fake_realtys: list[RealtyFake],
) -> list[Realty]:
    """Создание в БД объявлений о недвижимости"""
    new_realtys: list[Realty] = []
    for fake_realty, user in zip(fake_realtys, users, strict=False):
        realty_in = RealtySchemaCreate(**asdict(fake_realty))
        new_realty = await realty_crud.create(
            session, realty_in, user_id=user.id
        )  # TODO: create_many
        new_realtys.append(new_realty)

    return new_realtys


# Добавление пользователям избранным объявлений
@pytest.fixture
async def favorites_realtys(
    session: AsyncSession,
    users: list[User],
    realtys: list[Realty],
) -> list[Realty]:
    """Добавление всех объявлений кроме последнего в избранное первого пользователя
    с возвратом добавленных объявлений отфильтрованных по активности"""
    favorites_realtys: list[Realty] = []
    for realty in realtys[:-1]:
        favorite = UserRealtyFavorite(user_id=1, realty_id=realty.id)
        session.add(favorite)
        if realty.is_active:
            favorites_realtys.append(realty)
    await session.commit()

    return favorites_realtys
