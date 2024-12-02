from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, created_at, updated_at

if TYPE_CHECKING:
    from src.image.models import Image
    from src.user.models import User


class RealtyType(StrEnum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    COMMERCIAL = "COMMERCIAL"


class Realty(Base):
    __table_args__ = (
        CheckConstraint(
            "(type != 'Apartment' OR (floor IS NOT NULL AND rooms IS NOT NULL))",
            name="check_apartment_details",
        ),
    )

    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int]
    area: Mapped[int]
    floor: Mapped[int | None]
    rooms: Mapped[int | None]
    city: Mapped[str]
    state: Mapped[str]
    type: Mapped[RealtyType]
    is_active: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    update_at: Mapped[updated_at]

    user: Mapped["User"] = relationship(back_populates="realtys")

    title_image: Mapped["Image"] = relationship(
        back_populates="realty",
        primaryjoin="and_(Realty.id == Image.realty_id, Image.position == 0)",
        lazy="joined",
        viewonly=True,
    )
    images: Mapped[list["Image"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="realty",
        order_by="Image.position",
        overlaps="title_image",
    )
    followers: Mapped[list["User"]] = relationship(
        secondary="user_realty_favorites",
        back_populates="favorites",
        cascade="all",
    )

    repr_cols_num = 10
    repr_cols = ("created_at", "id")


class UserRealtyFavorite(Base):
    __table_args__ = (
        UniqueConstraint("user_id", "realty_id", name="idx_unique_user_realty"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    realty_id: Mapped[int] = mapped_column(ForeignKey("realtys.id", ondelete="CASCADE"))
