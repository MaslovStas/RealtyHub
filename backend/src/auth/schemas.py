from pydantic import (
    BaseModel,
    Field,
    field_validator,
)

from src.auth.constants import TokenType


class UserSchemaRefresh(BaseModel):
    """Схема пользователя refresh токена"""

    id: int = Field(alias="sub")
    type: TokenType = TokenType.REFRESH

    @field_validator("type")
    @classmethod
    def check_type(cls, v: TokenType) -> TokenType:
        default_type = cls.model_fields["type"].default
        if v != default_type:
            raise ValueError(
                f"Token`s type is {v.value}, expected {default_type.value}"
            )
        return v


class UserSchemaAccess(UserSchemaRefresh):
    """Схема пользователя из access токена"""

    type: TokenType = TokenType.ACCESS
    username: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
