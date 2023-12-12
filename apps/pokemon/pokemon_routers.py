from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E203
from config.database import get_session
from fastapi_filter import FilterDepends
from fastapi_pagination import LimitOffsetPage, Page

from apps.pokemon.api import get_pokemons, sync_pokemons
from apps.pokemon.filters import PokemonFilter
from apps.pokemon.schema import PokemonSchema


router = APIRouter(
    prefix="/v1",
    tags=["pokemons"],
    responses={404: {"description": "Not found"}},
)


@router.get("/pokemons", response_model=Page[PokemonSchema])
async def pokemons(
    session: AsyncSession = Depends(get_session),
    pokemon_filter: Optional[
        PokemonFilter
    ] = FilterDepends(PokemonFilter),
) -> LimitOffsetPage[PokemonSchema]:
    return await get_pokemons(session, pokemon_filter)


# TODO: Find a way to move this endpoint in migration
@router.post("/sync-pokemons")
async def add_pokemons(
    session: AsyncSession = Depends(get_session)
):
    return await sync_pokemons(session)
