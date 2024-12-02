from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import (
    authenticate_user,
    check_new_email_is_exists,
    get_current_user_for_refresh,
    http_bearer,
)
from src.auth.schemas import Token
from src.auth.utils import create_tokens
from src.core.database import get_session
from src.user.crud import user_crud
from src.user.models import User
from src.user.schemas import UserSchemaCreate

router = APIRouter(tags=["Auth"], dependencies=[Depends(http_bearer)])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    session: AsyncSession = Depends(get_session),
    user_in: UserSchemaCreate = Depends(check_new_email_is_exists),
) -> Token:
    """Регистрация нового пользователя"""
    new_user = await user_crud.create(session, user_in)
    token: Token = create_tokens(new_user)
    return token


@router.post("/token")
async def login_for_access_token(
    auth_user: User = Depends(authenticate_user),
) -> Token:
    """Аутентификация пользователя с получением токенов"""
    token: Token = create_tokens(auth_user)
    return token


@router.post("/refresh")
async def reissue_token(
    current_user: User = Depends(get_current_user_for_refresh),
) -> Token:
    """Перевыпуск токенов с помощью refresh токена"""
    token: Token = create_tokens(current_user)
    return token
