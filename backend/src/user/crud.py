from typing import cast

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.user.models import User
from src.user.schemas import UserSchemaCreate, UserSchemaUpdate


class CRUDUser:
    @staticmethod
    async def get(session: AsyncSession, user_id: int) -> User | None:
        user = await session.get(User, user_id)

        return user

    @staticmethod
    async def get_with_favorites(session: AsyncSession, user_id: int) -> User:
        stmt = select(User).filter_by(id=user_id).options(selectinload(User.favorites))
        result: Result[tuple[User]] = await session.execute(stmt)
        user = cast(User, result.scalar())

        return user

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        """Получение пользователя по email"""
        stmt = select(User).filter_by(email=email)
        result: Result[tuple[User]] = await session.execute(stmt)
        user = result.scalar()

        return user

    @staticmethod
    async def get_list(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        result: Result[tuple[User]] = await session.execute(stmt)
        users = result.scalars().all()

        return list(users)

    @staticmethod
    async def create(
        session: AsyncSession,
        user_in: UserSchemaCreate,
    ) -> User:
        new_user = User(**user_in.model_dump())
        session.add(new_user)
        await session.commit()

        return new_user

    @staticmethod
    async def create_many(
        session: AsyncSession,
        users_in: list[UserSchemaCreate],
    ) -> list[User]:
        new_users: list[User] = [User(**user_in.model_dump()) for user_in in users_in]
        session.add_all(new_users)
        await session.commit()

        return new_users

    @staticmethod
    async def update(
        session: AsyncSession,
        user: User,
        user_in: UserSchemaUpdate,
    ) -> User:
        for name, value in user_in.model_dump(exclude_none=True).items():
            if getattr(user, name) != value:
                setattr(user, name, value)
        await session.commit()

        return user

    @staticmethod
    async def delete(session: AsyncSession, user: User) -> None:
        await session.delete(user)
        await session.commit()


user_crud = CRUDUser()
