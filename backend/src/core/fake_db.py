import asyncio
from dataclasses import asdict
from random import randint, sample
from typing import Final

from src.core.database import Base, engine, session_factory
from src.fake_generators import RealtyFake, UserFake
from src.image.models import Image
from src.realty.crud import realty_crud
from src.realty.models import Realty, UserRealtyFavorite
from src.realty.schemas import RealtySchemaCreate
from src.user.crud import user_crud
from src.user.schemas import UserSchemaCreate


class FakeDB:
    NUMBER_USERS: Final[int] = 5
    NUMBER_REALTYS: Final[int] = NUMBER_USERS * 10
    MAX_NUMBER_IMAGES: Final[int] = 5
    NUMBER_FAVORITE_REALTYS: Final[int] = 5

    def __init__(self) -> None:
        self._engine = engine
        self._session_factory = session_factory

    async def init_db(self) -> None:
        print("->   init fake_db...")

        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def _add_users(self) -> None:
        """Заполнение таблицы users, где первый пользователь будет с заданным паролем"""
        print("->   add_users...")

        users_in: list[UserSchemaCreate] = []
        for i in range(self.NUMBER_USERS):
            is_test_user = i == 0  # Первый пользователь будет тестовым
            user_in = UserSchemaCreate(**asdict(UserFake(is_test_user=is_test_user)))
            users_in.append(user_in)

        async with self._session_factory() as session:
            await user_crud.create_many(session, users_in)

    async def _add_realtys(self) -> None:
        print("->   add_realtys...")

        async with self._session_factory() as session:
            for _ in range(self.NUMBER_REALTYS):
                user_id = randint(1, self.NUMBER_USERS)
                number_images = randint(0, self.MAX_NUMBER_IMAGES)
                realty_in = RealtySchemaCreate(
                    **asdict(RealtyFake(number_images=number_images))
                )
                realty = Realty(
                    **realty_in.model_dump(exclude={"images"}), user_id=user_id
                )
                images = [
                    Image(**image_in.model_dump(), position=position)
                    for position, image_in in enumerate(realty_in.images)
                ]
                realty.images = images

                session.add(realty)
            await session.commit()

    async def _add_follows(self) -> None:
        async with self._session_factory() as session:
            print("->   add_follow...")

            for user_id in range(1, self.NUMBER_USERS + 1):
                for realty_id in sample(
                    range(1, self.NUMBER_REALTYS + 1),
                    k=self.NUMBER_FAVORITE_REALTYS,
                ):
                    favorite = UserRealtyFavorite(user_id=user_id, realty_id=realty_id)
                    session.add(favorite)
            await session.commit()

    async def test(self) -> None:
        async with self._session_factory() as session:
            realtys = await realty_crud.get_created_user(session, user_id=1)
            print(realtys)

    async def create(self) -> None:
        await self.init_db()
        # await self._add_users()
        # await self._add_realtys()
        # await self._add_follows()


if __name__ == "__main__":
    asyncio.run(FakeDB().create())
    # asyncio.run(FakeDB().test())
