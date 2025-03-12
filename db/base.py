from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

engine = create_async_engine(
    url=str(settings.db.url),
    echo=False,  # Включение логирования SQL-запросов для отладки
    pool_size=20,  # Установка размера пула соединений
    max_overflow=10  # Максимальное количество дополнительных соединений
)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )
