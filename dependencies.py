from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import async_session_maker
from loguru import logger


async def get_session_with_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия с автоматическим коммитом."""
    async with async_session_maker() as session:
        try:
            logger.info("Создание асинхронной сессии с коммитом.")
            yield session
            await session.commit()
            logger.info("Коммит выполнен успешно.")
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при коммите: {e}")
            raise
        finally:
            await session.close()
            logger.info("Сессия закрыта.")


async def get_session_without_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия без автоматического коммита."""
    async with async_session_maker() as session:
        try:
            logger.info("Создание асинхронной сессии без коммита.")
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при работе с сессией: {e}")
            raise
        finally:
            await session.close()
            logger.info("Сессия закрыта.")
