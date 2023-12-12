from fastapi import FastAPI
from fastapi_pagination import add_pagination

from config.database import init_db
from apps.pokemon.pokemon_routers import router as pokemon_routers

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(pokemon_routers)

add_pagination(app)
