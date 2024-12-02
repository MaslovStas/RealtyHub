from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.realty.models import Realty


class Image(Base):
    url: Mapped[str]
    public_id: Mapped[str]
    position: Mapped[int]
    realty_id: Mapped[int] = mapped_column(ForeignKey("realtys.id", ondelete="CASCADE"))

    realty: Mapped["Realty"] = relationship(back_populates="images")

    repr_cols = ("id",)
