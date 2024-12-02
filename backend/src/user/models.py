from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, created_at, updated_at

if TYPE_CHECKING:
    from src.realty.models import Realty


class User(Base):
    username: Mapped[str]
    hashed_password: Mapped[bytes]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone: Mapped[str]
    created_at: Mapped[created_at]
    update_at: Mapped[updated_at]

    realtys: Mapped[list["Realty"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    favorites: Mapped[list["Realty"]] = relationship(
        secondary="user_realty_favorites",
        back_populates="followers",
        primaryjoin="and_("
        "User.id == UserRealtyFavorite.user_id,"
        "Realty.is_active == True)",
        cascade="all",
    )
