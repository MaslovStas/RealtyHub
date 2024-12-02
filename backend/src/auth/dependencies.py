from collections.abc import Callable, Coroutine
from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import EmailAlreadyExists, NotAuthenticated, PermissionDenied
from src.auth.schemas import UserSchemaAccess, UserSchemaRefresh
from src.auth.security import validate_password
from src.auth.utils import decode_jwt
from src.core.database import get_session
from src.exceptions import NotFound
from src.user.crud import user_crud
from src.user.models import User
from src.user.schemas import UserSchemaCreate, UserSchemaUpdate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/jwt/token", auto_error=False)
http_bearer = HTTPBearer(auto_error=False)


async def check_new_email_is_exists(
    user_in: UserSchemaCreate,
    session: AsyncSession = Depends(get_session),
) -> UserSchemaCreate:
    """Проверка на существование email в БД или вызов ошибки"""
    existing_user = await user_crud.get_by_email(session, user_in.email)
    if existing_user:
        raise EmailAlreadyExists

    return user_in


async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> User:
    """Получение пользователя по id"""
    user = await user_crud.get(session, user_id)
    if not user:
        raise NotFound(detail=f"User id={user_id} not found")

    return user


async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
) -> User | None:
    """Аутентификация пользователя по email и паролю или вызов ошибки"""
    user = await user_crud.get_by_email(session, form_data.username)
    if user and validate_password(form_data.password, user.hashed_password):
        return user

    raise NotAuthenticated(detail="Invalid username or password")


def get_payload_from_token(
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    """Получение и декодирование данных из токена в заголовке запроса"""
    if not token:
        raise NotAuthenticated
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as error:
        raise NotAuthenticated(detail="Could not validate credentials") from error

    return payload


def get_current_user_from_token[SchemaType: (UserSchemaRefresh, UserSchemaAccess)](
    schema: type[SchemaType],
) -> Callable[[str, AsyncSession], Coroutine[Any, Any, User]]:
    async def wrapper(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session),
    ) -> User:
        """Фабричная функция получения текущего пользователя из токена"""
        payload: dict[str, Any] = get_payload_from_token(token)
        try:
            current_user_info = schema(**payload)
        except ValueError as error:
            raise NotAuthenticated from error

        current_user: User = await get_user_by_id(current_user_info.id, session)
        return current_user

    return wrapper


# Получение данных о пользователе из access токена
get_current_user = get_current_user_from_token(UserSchemaAccess)

# Получение данных о пользователе из refresh токена
get_current_user_for_refresh = get_current_user_from_token(UserSchemaRefresh)


async def get_current_user_or_none(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User | None:
    try:
        current_user = await get_current_user(token, session)
    except (NotAuthenticated, NotFound, ValueError):
        return None

    return current_user


async def get_user_by_id_for_current_user(
    current_user: User = Depends(get_current_user), user: User = Depends(get_user_by_id)
) -> User:
    """Получение пользователя по id со сравнением его с текущим пользователем"""
    if current_user is not user:
        raise PermissionDenied

    return user


async def check_update_email_is_exists(
    user_in: UserSchemaUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> UserSchemaUpdate:
    """Проверка на существование email в БД или вызов ошибки"""
    if user_in.email and user_in.email != current_user.email:
        existing_user = await user_crud.get_by_email(session, user_in.email)
        if existing_user is not None:
            raise EmailAlreadyExists

    return user_in
