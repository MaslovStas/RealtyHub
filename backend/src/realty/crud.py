from typing import cast

from sqlalchemy import Result, Select, asc, case, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, noload, selectinload

from src.image.models import Image
from src.image.schemas import ImageSchemaUpdate
from src.image.services import delete_images
from src.realty.models import Realty, UserRealtyFavorite
from src.realty.schemas import (
    RealtySchemaCreate,
    RealtySchemaFilter,
    RealtySchemaUpdate,
)

# T = TypeVar("T", Realty, int, tuple[Realty, bool])


class CRUDRealty:
    @staticmethod
    async def get(session: AsyncSession, realty_id: int) -> Realty | None:
        """Получение объявления по id"""
        stmt = (
            select(Realty)
            .filter_by(id=realty_id)
            .options(
                selectinload(Realty.images),
                joinedload(Realty.user),
                noload(Realty.title_image),
            )
        )
        result: Result[tuple[Realty]] = await session.execute(stmt)
        realty = result.scalar()

        return realty

    async def get_list(
        self,
        session: AsyncSession,
        filter_query: RealtySchemaFilter = RealtySchemaFilter(),
    ) -> list[Realty]:
        """Получение списка объявлений по заданному фильтру"""
        stmt = select(Realty).options(joinedload(Realty.title_image))

        stmt = self._applying_search_filters(stmt, filter_query)
        stmt = self._applying_offset_limit_order_filters(stmt, filter_query)

        result: Result[tuple[Realty]] = await session.execute(stmt)
        realtys = result.scalars().all()

        return list(realtys)

    async def get_list_with_is_favorite(
        self,
        session: AsyncSession,
        user_id: int,
        filter_query: RealtySchemaFilter = RealtySchemaFilter(),
    ) -> list[Realty]:
        """Получение списка объявлений по заданному фильтру с данными о том, являются
        ли объявления избранными для текущего пользователя"""

        stmt = select(
            Realty,
            case((UserRealtyFavorite.user_id.isnot(None), True), else_=False).label(
                "is_favorite"
            ),
        ).outerjoin(
            UserRealtyFavorite,
            (
                (UserRealtyFavorite.realty_id == Realty.id)
                & (UserRealtyFavorite.user_id == user_id)
            ),
        )

        stmt = self._applying_search_filters(stmt, filter_query)
        stmt = self._applying_offset_limit_order_filters(stmt, filter_query)

        result: Result[tuple[Realty, bool]] = await session.execute(stmt)

        realtys: list[Realty] = []
        for row in result.all():
            realty, is_favorite = row
            realty.is_favorite = is_favorite
            realtys.append(realty)

        return realtys

    async def get_count_list(
        self,
        session: AsyncSession,
        filter_query: RealtySchemaFilter = RealtySchemaFilter(),
    ) -> int:
        """Получение количества объявлений для поискового фильтра"""
        stmt = select(func.count()).select_from(Realty)
        stmt = self._applying_search_filters(stmt, filter_query)
        result: Result[tuple[int]] = await session.execute(stmt)
        total = cast(int, result.scalar())

        return total

    @staticmethod
    async def get_favorites(session: AsyncSession, user_id: int) -> list[Realty]:
        stmt = (
            select(Realty)
            .join(UserRealtyFavorite)
            .filter(
                UserRealtyFavorite.user_id == user_id,
                Realty.is_active,
            )
        )
        result: Result[tuple[Realty]] = await session.execute(stmt)
        favorites = result.scalars().all()

        return list(favorites)

    @staticmethod
    async def get_count_favorites(session: AsyncSession, user_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(UserRealtyFavorite)
            .join(Realty)
            .filter(
                UserRealtyFavorite.user_id == user_id,
                Realty.is_active,
            )
        )
        result: Result[tuple[int]] = await session.execute(stmt)
        total = cast(int, result.scalar())

        return total

    @staticmethod
    async def _get_user_realty_favorite(
        session: AsyncSession,
        user_id: int,
        realty_id: int,
    ) -> UserRealtyFavorite | None:
        stmt = select(UserRealtyFavorite).filter_by(
            user_id=user_id, realty_id=realty_id
        )
        result: Result[tuple[UserRealtyFavorite]] = await session.execute(stmt)
        favorite: UserRealtyFavorite | None = result.scalar()

        return favorite

    @staticmethod
    async def get_created_user(
        session: AsyncSession,
        user_id: int,
    ) -> list[Realty]:
        stmt = select(Realty).filter_by(user_id=user_id).order_by("created_at")
        result: Result[tuple[Realty]] = await session.execute(stmt)
        realtys = result.scalars().all()

        return list(realtys)

    async def follow_favorite(
        self,
        session: AsyncSession,
        user_id: int,
        realty_id: int,
    ) -> None:
        favorite = await self._get_user_realty_favorite(session, user_id, realty_id)
        if favorite is None:
            session.add(UserRealtyFavorite(user_id=user_id, realty_id=realty_id))
            await session.commit()

    async def unfollow_favorite(
        self,
        session: AsyncSession,
        user_id: int,
        realty_id: int,
    ) -> None:
        favorite = await self._get_user_realty_favorite(session, user_id, realty_id)
        if favorite is not None:
            await session.delete(favorite)
            await session.commit()

    @staticmethod
    def _applying_search_filters[T: (Realty, int, tuple[Realty, bool])](
        stmt: Select[tuple[T]], filter_query: RealtySchemaFilter
    ) -> Select[tuple[T]]:
        """Применение поисковых фильтров для объявлений"""
        if filter_query.min_price is not None:
            stmt = stmt.filter(Realty.price >= filter_query.min_price)

        if filter_query.max_price is not None:
            stmt = stmt.filter(Realty.price <= filter_query.max_price)

        if filter_query.city is not None:
            stmt = stmt.filter(Realty.city.like(f"%{filter_query.city.lower()}%"))

        if filter_query.with_photos:
            stmt = stmt.filter(Realty.images.any())

        if filter_query.rooms is not None:
            if filter_query.rooms >= 5:
                stmt = stmt.filter(Realty.rooms >= filter_query.rooms)
            else:
                stmt = stmt.filter(Realty.rooms == filter_query.rooms)

        if filter_query.type is not None:
            stmt = stmt.filter(Realty.type == filter_query.type)

        if filter_query.is_active:
            stmt = stmt.filter(Realty.is_active)

        return stmt

    @staticmethod
    def _applying_offset_limit_order_filters(
        stmt: Select[tuple[Realty]], filter_query: RealtySchemaFilter
    ) -> Select[tuple[Realty]]:
        """Применение limit, offset и order из поискового фильтра для объявлений"""
        field_order = getattr(Realty, filter_query.order_by)
        order = desc if filter_query.desc_order else asc

        stmt = (
            stmt.order_by(order(field_order))
            .offset(filter_query.offset)
            .limit(filter_query.limit)
        )

        return stmt

    async def create(
        self,
        session: AsyncSession,
        realty_in: RealtySchemaCreate,
        user_id: int,
    ) -> Realty:
        new_realty = self._init_realty_ORM_from_realty_in(realty_in, user_id)
        session.add(new_realty)
        await session.commit()

        return new_realty

    @staticmethod
    def _init_realty_ORM_from_realty_in(
        realty_in: RealtySchemaCreate, user_id: int
    ) -> Realty:
        new_realty = Realty(**realty_in.model_dump(exclude={"images"}), user_id=user_id)
        new_realty.images = [
            Image(**image_in.model_dump(), position=position)
            for position, image_in in enumerate(realty_in.images)
        ]

        return new_realty

    @staticmethod
    async def update(
        session: AsyncSession,
        realty: Realty,
        realty_in: RealtySchemaUpdate,
    ) -> Realty:
        # Обновляем фотографии объявления, если они переданы
        if realty_in.images:
            existing_images: dict[int, Image] = {
                image.id: image for image in realty.images
            }
            images_in: list[ImageSchemaUpdate] = realty_in.images

            for position, image_in in enumerate(images_in):
                if image_in.id is None:  # Новое фото
                    new_image = Image(
                        **image_in.model_dump(exclude_none=True),
                        position=position,
                    )
                    realty.images.append(new_image)

                elif existing_image := existing_images.get(
                    image_in.id
                ):  # если id найден, обновляем фото
                    for name, value in image_in.model_dump(exclude={"id"}).items():
                        if getattr(existing_image, name) != value:
                            setattr(existing_image, name, value)
                    # Обновляем позицию объявления
                    if existing_image.position != position:
                        existing_image.position = position
                    # После обновления фото, удаляем его из словаря
                    existing_images.pop(image_in.id)
            # Удаляем оставшиеся фото в словаре из БД и сервера
            public_ids_need_to_delete = []
            for image in existing_images.values():
                public_ids_need_to_delete.append(image.public_id)
                realty.images.remove(image)

            delete_images(public_ids_need_to_delete)
        # Обновляем объявление
        for name, value in realty_in.model_dump(
            exclude_none=True, exclude={"images"}
        ).items():
            if getattr(realty, name) != value:
                setattr(realty, name, value)

        await session.commit()
        await session.refresh(realty, attribute_names=["images"])

        return realty

    @staticmethod
    async def delete(session: AsyncSession, realty: Realty) -> None:
        await session.delete(realty)
        await session.commit()

        delete_images([image.public_id for image in realty.images])


realty_crud = CRUDRealty()
