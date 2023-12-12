from fastapi import Depends, FastAPI
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E203
from config.database import get_session, init_db  # noqa: E203
from fastapi_filter import FilterDepends
from fastapi_pagination import LimitOffsetPage, add_pagination

from apps.pokemon.api import get_pokemons, sync_pokemons
from apps.pokemon.filters import PokemonFilter
from apps.pokemon.schema import PokemonSchema


app = FastAPI()
add_pagination(app)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/v1/pokemons")
async def pokemons(
    session: AsyncSession = Depends(get_session),
    pokemon_filter: Optional[
        PokemonFilter
    ] = FilterDepends(PokemonFilter),
) -> LimitOffsetPage[PokemonSchema]:
    return await get_pokemons(session, pokemon_filter)


# TODO: Find a way to move this endpoint in migration
@app.post("/v1/sync-pokemons")
async def add_pokemons(
    session: AsyncSession = Depends(get_session)
):
    return await sync_pokemons(session)
