from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.auth.exceptions import PermissionDenied
from src.core.database import get_session
from src.exceptions import NotFound
from src.realty.crud import realty_crud
from src.realty.models import Realty
from src.user.models import User


async def get_realty_by_id(
    realty_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(get_session),
) -> Realty:
    realty = await realty_crud.get(session, realty_id)
    if not realty:
        raise NotFound(detail=f"Realty id={realty_id} not found")

    return realty


async def get_realty_by_id_for_current_user(
    realty: Realty = Depends(get_realty_by_id),
    current_user: User = Depends(get_current_user),
) -> Realty:
    if current_user is not realty.user:
        raise PermissionDenied

    return realty
