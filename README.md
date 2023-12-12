# List pokemons
A app to list and filter pokemons.

## Initialize environment

Create a `.env` file in the project folder. (For development, blank file is fine).
Copy `.env.example` if you want to modify database credentials.

```bash
cp .env.example .env
```

## Get started with:

```bash
docker-compose up --build -d
```

## Browseable api links

Navigate to `localhost:8002/docs` to view available endpoints

## Sync pokemons from API to database

Use this command to populate pokemons in database.

```bash
curl -X 'POST' \
  'http://localhost:8002/v1/sync-pokemons' \
  -H 'accept: application/json' \
  -d ''
```
Or from browseable API you can populate pokemons by using `sync-pokemons` endpoint. 
