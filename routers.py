from fastapi import APIRouter
from transformers import BlipProcessor, BlipForConditionalGeneration
from fastapi import UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import Image
from io import BytesIO
from typing import Tuple
from loguru import logger
from crud import create_history, get_histories
from dependencies import get_session_with_commit, get_session_without_commit
from history_schemas import SRequestHistory


logger.add("logs/error.log", level="ERROR", format="{time} - {level} - {message}")

router = APIRouter()


processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


@router.post("/generate_caption/")
async def generate_caption(file: UploadFile = File(...)):
    """
       Генерирует текстовое описание для загруженного изображения.

       Args:
           file (UploadFile): Изображение, загруженное пользователем.

       Returns:
           dict: Словарь с ключом "description", содержащим текстовое описание изображения.
                В случае ошибки возвращает словарь с ключом "error" и описанием проблемы.
       """
    logger.info(f"Получен запрос на генерацию описания для файла {file.filename}")
    try:
        # Загрузка изображения
        contents = await file.read()
        raw_image = Image.open(BytesIO(contents)).convert("RGB")
        logger.debug(f"Изображение успешно загружено и преобразовано")

        # Генерация описания
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        logger.success(f"Описание успешно сгенерировано: {caption}")

        return {"description": caption}
    except Exception as e:
        logger.error(f"Ошибка при обработке изображения: {str(e)}")
        return {"error": str(e)}


@router.post("/generate_caption_with_history/")
async def generate_caption_with_history(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
       Генерирует текстовое описание для загруженного изображения и сохраняет историю запроса в базе данных.

       Args:
           file (UploadFile): Изображение, загруженное пользователем.
           session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

       Returns:
           dict: Словарь с ключами "id" и "description", содержащими ID созданной записи и текстовое описание изображения.
                В случае ошибки вызывает HTTP-исключение с кодом 500.
       """
    logger.info(f"Получен запрос на генерацию описания с сохранением истории для файла {file.filename}")

    async def process_image(contents: bytes) -> Tuple[bytes, str]:
        """
        Внутренняя асинхронная функция для обработки изображения и генерации описания.

        Args:
            contents (bytes): Байтовое представление изображения.

        Returns:
            Tuple[bytes, str]: Кортеж, содержащий байты изображения и его текстовое описание.
        """
        raw_image = Image.open(BytesIO(contents)).convert("RGB")
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return raw_image.tobytes(), caption

    try:
        contents = await file.read()
        image_data, caption = await process_image(contents)

        # Создание новой записи в базе данных
        new_request = SRequestHistory(
            image_data=image_data,
            description=caption,
        )
        request = await create_history(session, new_request)
        logger.success(f"Запись истории успешно создана с ID: {request.id}")

        return {"id": request.id, "description": caption}
    except Exception as e:
        logger.error(f"Ошибка при создании записи истории: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@router.get("/histories/")
async def get_history(session: AsyncSession = Depends(get_session_without_commit)):
    """
       Возвращает историю всех запросов на генерацию описаний изображений.

       Args:
           session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

       Returns:
           list: Список словарей с информацией о каждой записи:
                - "id": ID записи.
                - "description": Текстовое описание изображения.
                - "created_at": Дата и время создания записи.
       """
    logger.info("Получен запрос на получение истории запросов")

    try:
        history = await get_histories(session)
        result = [
            {
                "id": item.id,
                "description": item.description,
                "created_at": item.created_at.isoformat()
            }
            for item in history
        ]
        logger.success(f"Найдено {len(result)} записей в истории запросов")
        return result
    except Exception as e:
        logger.error(f"Ошибка при получении истории запросов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")
