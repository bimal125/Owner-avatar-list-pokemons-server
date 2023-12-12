import requests
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi_pagination import paginate

from apps.pokemon.models import (
    Pokemon, PokemonImage, PokemonType
)


async def get_pokemons(session, pokemon_filter):
    result = await session.execute(
        pokemon_filter.filter(
            select(Pokemon).options(
                selectinload(Pokemon.images)
            ).options(
                selectinload(Pokemon.types)
            ).outerjoin(PokemonType)
        )
    )
    return paginate(result.scalars().all())


async def sync_pokemons(session):
    response = requests.get(
        'https://pokeapi.co/api/v2/pokemon'
    )

    def extract_images(obj):
        images = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'front_default' or key == 'front_female':
                    if value:
                        images.append(value)
                elif isinstance(value, (dict, list)):
                    if value:
                        images.extend(extract_images(value))
        elif isinstance(obj, list):
            for item in obj:
                images.extend(extract_images(item))
        return images

    pokemons = response.json()
    for pokemon in pokemons['results']:
        response = requests.get(pokemon.get('url'))
        pokemon_detail = response.json()

        # TODO: Find better way to handle database transactions
        try:
            pokemon = Pokemon(
                name=pokemon_detail['name'],
            )
            session.add(pokemon)
            await session.commit()
            await session.refresh(pokemon)
            type_names = [
                item['type']['name'] for item in pokemon_detail['types']
            ]
            # Save 4 types at most
            for pokemon_type in type_names[:4]:
                pokemon_type = PokemonType(
                    type=pokemon_type, pokemon_id=pokemon.id
                )
                session.add(pokemon_type)

            sprites = pokemon_detail['sprites']
            images = extract_images(sprites)

            # Save 4 images at most
            for image in images[:4]:
                pokemon_image = PokemonImage(
                    image=image, pokemon_id=pokemon.id
                )
                session.add(pokemon_image)
        except requests.exceptions.ConnectionError:
            raise
        finally:
            await session.commit()
            session.close()

    return {'message': 'Synced pokemons'}
