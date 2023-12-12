from typing import Optional
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from apps.pokemon.models import Pokemon, PokemonType


class PokemonTypeFilter(Filter):
    type__in: Optional[list[str]] = None

    class Constants(Filter.Constants):
        model = PokemonType


class PokemonFilter(Filter):
    name: Optional[str] = None
    types: Optional[PokemonTypeFilter] = FilterDepends(
        with_prefix("types", PokemonTypeFilter)
    )

    class Constants(Filter.Constants):
        model = Pokemon
