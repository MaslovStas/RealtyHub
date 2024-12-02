from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
)

from src.auth.security import hash_password


class UserSchemaBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    phone: str


class UserSchemaUpdate(BaseModel):
    username: str | None = Field(min_length=3, max_length=20, default=None)
    email: EmailStr | None = None
    phone: str | None = None
    password: str | None = Field(default=None, exclude=True)

    @computed_field
    def hashed_password(self) -> bytes | None:
        return hash_password(self.password) if self.password else None


class UserSchemaCreate(UserSchemaBase):
    password: str = Field(exclude=True)

    @computed_field
    def hashed_password(self) -> bytes:
        return hash_password(self.password)


class UserSchema(UserSchemaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
