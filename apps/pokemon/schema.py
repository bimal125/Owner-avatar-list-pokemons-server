from pydantic import BaseModel
from typing import Optional, List


class PokemonImageSchema(BaseModel):
    id: int
    image: Optional[str]

    class Config:
        from_attributes = True


class PokemonTypeSchema(BaseModel):
    id: int
    type: Optional[str]

    class Config:
        from_attributes = True


class PokemonSchema(BaseModel):
    id: int
    name: str
    images: List[PokemonImageSchema]
    types: List[PokemonTypeSchema]

    class Config:
        from_attributes = True
