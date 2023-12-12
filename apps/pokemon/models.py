from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from config.database import Base


class Pokemon(Base):
    __tablename__ = 'pokemons'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    images: Mapped[List["PokemonImage"]] = relationship(
        back_populates="pokemon", cascade="all, delete-orphan"
    )
    types: Mapped[List["PokemonType"]] = relationship(
        back_populates="pokemon", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Pokemon(name={self.name!r}"


class PokemonImage(Base):
    __tablename__ = 'pokemon_images'

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String(255))
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id"))
    pokemon: Mapped["Pokemon"] = relationship(back_populates="images")

    def __repr__(self) -> str:
        return f"PokemonImage(image={self.image!r}"


class PokemonType(Base):
    __tablename__ = 'pokemon_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(255))
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id"))
    pokemon: Mapped["Pokemon"] = relationship(back_populates="types")

    def __repr__(self) -> str:
        return f"PokemonType(image={self.type!r}"
