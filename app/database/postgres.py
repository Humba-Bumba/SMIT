from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models.rate import Base
from config.settings import settings

user = settings.postgres_user
password = settings.postgres_password
host = settings.postgres_host
port = settings.postgres_port
db_name = settings.postgres_db

DATABASE_URI = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'
engine = create_async_engine(DATABASE_URI, echo=True, future=True)
async_session = sessionmaker(engine=engine, class_=AsyncSession, expire_on_commit=False)

sync_DATABASE_URI = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
sync_engine = create_engine(sync_DATABASE_URI, echo=True, future=True)


def init_db():
    Base.metadata.create_all(bind=sync_engine)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
