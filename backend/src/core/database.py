import re
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from src.config import settings

engine = create_async_engine(
    url=settings.db.DATABASE_URL,
    echo=settings.db.ECHO_DB,
)
session_factory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

created_at = Annotated[
    datetime,
    mapped_column(default=datetime.now(tz=UTC), server_default=func.now()),
]
updated_at = Annotated[
    datetime,
    mapped_column(default=datetime.now(tz=UTC), server_default=func.now()),
]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Преобразование из имени класса в название таблицы"""
        tablename: str = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower() + "s"
        return tablename

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    repr_cols_num = 3
    repr_cols: tuple[str, ...] = ()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
