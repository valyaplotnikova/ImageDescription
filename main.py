from contextlib import asynccontextmanager
from typing import AsyncGenerator
from loguru import logger
from fastapi import FastAPI, APIRouter
from routers import router as image_router


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("Инициализация приложения...")
    yield
    logger.info("Завершение работы приложения...")


def create_app() -> FastAPI:
    """
   Создание и конфигурация FastAPI приложения.

   Returns:
       Сконфигурированное приложение FastAPI
   """
    app = FastAPI(
        title="Микросервис для работы с пользователями, командами, проектами и организационной структурой",
        lifespan=lifespan,
    )

    # Регистрация роутеров
    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    """Регистрация роутеров приложения."""
    # Корневой роутер
    root_router = APIRouter()

    @root_router.get("/", tags=["root"])
    def home_page():
        return {
            "message": "Добро пожаловать в  сервис для описания изображений!",
        }

    # Подключение роутеров
    app.include_router(root_router, tags=["root"])
    app.include_router(image_router, tags=["image_caption"])


# Создание экземпляра приложения
app = create_app()
