from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.image.schemas import ImageSchema, ImageSchemaCreate, ImageSchemaUpdate
from src.realty.models import RealtyType


class RealtySchemaBase(BaseModel):
    title: str
    description: str
    price: int = Field(ge=0)
    area: int = Field(gt=0)
    floor: int | None = Field(gt=0, default=None)
    rooms: int | None = Field(gt=0, default=None)
    city: str
    state: str
    type: RealtyType
    is_active: bool = True


class RealtySchemaCreate(RealtySchemaBase):
    images: list[ImageSchemaCreate]

    @model_validator(mode="after")
    def check_is_apartment(self) -> Self:
        if self.type == RealtyType.APARTMENT:
            if self.floor is None:
                raise ValueError("Not specified floor")
            if self.rooms is None:
                raise ValueError("Not specified rooms")
        else:
            self.floor = None
            self.rooms = None

        return self


class RealtySchemaUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    area: int | None = Field(gt=0, default=None)
    price: int | None = Field(ge=0, default=None)
    floor: int | None = Field(gt=0, default=None)
    rooms: int | None = Field(gt=0, default=None)
    city: str | None = None
    state: str | None = None
    type: RealtyType
    is_active: bool | None = None

    images: list[ImageSchemaUpdate] | None = None

    @model_validator(mode="after")
    def check_is_not_apartment(self) -> Self:
        """Если не Apartment, то необходимо обнулить этаж и комнаты"""
        if self.type != RealtyType.APARTMENT:
            self.floor = None
            self.rooms = None
        return self


class RealtySchema(RealtySchemaBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class RealtySchemaShort(RealtySchema):
    title_image: ImageSchema | None
    is_favorite: bool | None = None


class RealtySchemaFull(RealtySchema):
    images: list[ImageSchema]


class RealtySchemaFilter(BaseModel):
    limit: int = Field(default=100, gt=0, le=100)
    offset: int = Field(default=0, ge=0)
    is_active: bool = True
    min_price: int | None = Field(ge=0, default=None)
    max_price: int | None = Field(ge=0, default=None)
    rooms: int | None = Field(gt=0, default=None)
    city: str | None = None
    type: RealtyType | None = None
    with_photos: bool = False
    order_by: Literal["created_at", "price"] = "created_at"
    desc_order: bool = True

    @field_validator("type", mode="before")
    @classmethod
    def convert_to_title(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.upper()
        return v

    @model_validator(mode="after")
    def check_prices(self) -> Self:
        """Проверка, что минимальная цена не может быть больше максимальной"""
        if (
            self.min_price is not None
            and self.max_price is not None
            and self.min_price > self.max_price
        ):
            raise ValueError("Price min can`t be more price max")
        return self
