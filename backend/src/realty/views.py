from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, get_current_user_or_none
from src.core.database import get_session
from src.realty.crud import realty_crud
from src.realty.dependecies import (
    get_realty_by_id,
    get_realty_by_id_for_current_user,
)
from src.realty.models import Realty
from src.realty.schemas import (
    RealtySchemaCreate,
    RealtySchemaFilter,
    RealtySchemaFull,
    RealtySchemaShort,
    RealtySchemaUpdate,
)
from src.user.models import User

router = APIRouter(
    tags=["Realtys"],
)


@router.get("/", response_model=list[RealtySchemaShort])
async def get_realtys(
    response: Response,
    filter_query: Annotated[RealtySchemaFilter, Query()],
    session: AsyncSession = Depends(get_session),
    current_user: User | None = Depends(get_current_user_or_none),
) -> list[Realty]:
    if current_user:
        realtys = await realty_crud.get_list_with_is_favorite(
            session,
            current_user.id,
            filter_query,
        )
    else:
        realtys = await realty_crud.get_list(session, filter_query)
    total_realtys = await realty_crud.get_count_list(session, filter_query)
    response.headers["X-Total-Count"] = str(total_realtys)
    return realtys


@router.get("/{realty_id}/", response_model=RealtySchemaFull)
async def get_realty(realty: Realty = Depends(get_realty_by_id)) -> Realty:
    return realty


@router.post(
    "/",
    response_model=RealtySchemaFull,
    status_code=status.HTTP_201_CREATED,
)
async def create_realty(
    realty_in: RealtySchemaCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Realty:
    new_realty = await realty_crud.create(session, realty_in, current_user.id)
    return new_realty


@router.patch("/{realty_id}/", response_model=RealtySchemaFull)
async def update_realty(
    realty_in: RealtySchemaUpdate,
    realty: Realty = Depends(get_realty_by_id_for_current_user),
    session: AsyncSession = Depends(get_session),
) -> Realty:
    updated_realty = await realty_crud.update(session, realty, realty_in)
    return updated_realty


@router.delete("/{realty_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_realty(
    realty: Realty = Depends(get_realty_by_id_for_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    await realty_crud.delete(session, realty)


@router.get(
    "/favorites",
    status_code=status.HTTP_200_OK,
    response_model=list[RealtySchemaShort],
)
async def get_favorites_realty(
    response: Response,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[Realty]:
    favorites = await realty_crud.get_favorites(session, current_user.id)
    total_favorites = await realty_crud.get_count_favorites(session, current_user.id)
    response.headers["X-Total-Count"] = str(total_favorites)
    return favorites


@router.post("/favorites/{realty_id}/", status_code=status.HTTP_201_CREATED)
async def follow_realty(
    current_user: User = Depends(get_current_user),
    realty: Realty = Depends(get_realty_by_id),
    session: AsyncSession = Depends(get_session),
) -> None:
    await realty_crud.follow_favorite(session, current_user.id, realty.id)


@router.delete("/favorites/{realty_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_realty(
    current_user: User = Depends(get_current_user),
    realty: Realty = Depends(get_realty_by_id),
    session: AsyncSession = Depends(get_session),
) -> None:
    await realty_crud.unfollow_favorite(session, current_user.id, realty.id)
