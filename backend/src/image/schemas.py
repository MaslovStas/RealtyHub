from pydantic import BaseModel, ConfigDict


class ImageSchemaBase(BaseModel):
    url: str
    public_id: str


class ImageSchemaCreate(ImageSchemaBase):
    pass


class ImageSchemaUpdate(ImageSchemaBase):
    id: int | None = None


class ImageSchema(ImageSchemaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
