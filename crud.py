from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from db.models import RequestHistory
from history_schemas import SRequestHistory


@logger.catch
async def create_history(
        db: AsyncSession,
        history: SRequestHistory):

    logger.info(f"Создание новой записи RequestHistory")

    try:
        db_history = RequestHistory(**history.dict())
        db.add(db_history)
        await db.commit()
        await db.refresh(db_history)
        logger.success(f"Запись RequestHistory успешно создана с ID: {db_history.id}")
        return db_history
    except Exception as e:
        logger.error(f"Ошибка при создании записи RequestHistory: {e}")
        raise


@logger.catch
async def get_history(db: AsyncSession, history_id: int):
    logger.info(f"Получение записи RequestHistory по ID: {history_id}")

    try:
        history = await db.execute(
            select(RequestHistory).where(RequestHistory.id == history_id)
        )
        result = history.scalar_one_or_none()
        if result:
            logger.debug(f"Найдена запись RequestHistory с ID: {result.id}")
        else:
            logger.warning(f"Запись RequestHistory с ID {history_id} не найдена")
        return result
    except Exception as e:
        logger.error(f"Ошибка при получении записи RequestHistory по ID {history_id}: {e}")
        raise


@logger.catch
async def get_histories(db: AsyncSession):
    logger.info("Получение всех записей RequestHistory")

    try:
        histories = await db.execute(
            select(RequestHistory.id, RequestHistory.description, RequestHistory.created_at)
        )
        result = histories.all()
        logger.debug(f"Найдено {len(result)} записей RequestHistory")
        return result
    except Exception as e:
        logger.error(f"Ошибка при получении всех записей RequestHistory: {e}")
        raise
