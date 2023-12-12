from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from config.database import init_db
from apps.pokemon.pokemon_routers import router as pokemon_routers

app = FastAPI()

ORIGINS = [
    # Localhost
    "http://localhost:3080",
    "http://127.0.0.1:3080",
]

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'sentry-trace',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)


@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(pokemon_routers)

add_pagination(app)
