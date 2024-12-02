from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import (
    check_update_email_is_exists,
    get_current_user,
    get_user_by_id_for_current_user,
)
from src.core.database import get_session
from src.realty.crud import realty_crud
from src.realty.models import Realty
from src.realty.schemas import RealtySchemaShort
from src.user.crud import user_crud
from src.user.models import User
from src.user.schemas import UserSchema, UserSchemaUpdate

router = APIRouter(tags=["User"])


@router.get("/me/realtys", response_model=list[RealtySchemaShort])
async def get_users_realtys(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[Realty]:
    return await realty_crud.get_created_user(session, current_user.id)


@router.get("/me/", response_model=UserSchema)
async def read_current_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Получение данных о текущем пользователе"""
    return current_user


@router.patch("/{user_id}/", response_model=UserSchema)
async def update_user(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_user_by_id_for_current_user),
    user_in: UserSchemaUpdate = Depends(check_update_email_is_exists),
) -> User:
    """Обновление профайла пользователя"""
    return await user_crud.update(session, user, user_in)
