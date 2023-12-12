import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'postgresqlpwd')
postgres_host = os.environ.get('POSTGRES_HOST', 'db')
postgres_db = os.environ.get('POSTGRES_DB', 'postgres')
postgres_port = os.environ.get('POSTGRES_PORT', 5432)


DATABASE_URL = 'postgresql+asyncpg://{user}:{pwd}@{host}:{port}/{name}'.format(
    user=postgres_user,
    pwd=postgres_password,
    host=postgres_host,
    port=postgres_port,
    name=postgres_db,
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

meta = MetaData()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


Base = declarative_base()
