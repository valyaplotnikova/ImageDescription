# Сервис для описания изображений
## Описание
Сервис на Python, который принимает изображение и возвращает его текстовое описание

## Структура проекта
```plaintext
ImageDescription/
├── .env.example 
├── alembic.ini  
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── routers.py  
├── history_schemas.py 
├── main.py
├── crud.py
├── dependencies.py
├── config.py
└── alembic/
└── db/
    ├── models.py
    ├── base.py
└── logs/
   
```
## Зависимости
alembic-1.15.1    
asyncpg-0.30.0  
fastapi-0.115.11  
gradio-5.20.1  
SQLAlchemy-2.0.38  
loguru-0.7.3  
torch-2.6.0  
transformers-4.49.0  
pillow-11.1.0  
pydantic-2.10.6  
pydantic-settings-2.8.1  
python-dotenv-1.0.1  
uvicorn-0.34.0

## Установка

1. Клонируйте данный репозиторий к себе на локальную машину: git clone https://github.com/valyaplotnikova/OrgManager.git

2. В файле .env.example подставьте свои переменные окружения и переименуйте файлы в .env

3. Запустите Docker   
Введите команду в терминале:    

Для Compose V1:

```
docker-compose up -d --build 
```
Для Compose V2:
```
docker compose up -d --build 
```
4. Сервис готов для использования на - http://localhost:8000


Документация доступна на - http://localhost:8000/docs



## Локальный запуск для разработки

Для локального запуска сервиса необходимо создать виртуальное окружение
python -m venv .venv
Активация виртуальной среды для OC Linux
```bash
source .venv/bin/activate
```
Активация виртуальной среды для OC Windows
```bash
venv\Scripts\activate
```
Далее, нужно установить зависимости:
```bash
pip install -r requirements.txt
```
Запуск API
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
Интерфейс Gradio можно запустить отдельно:
```bash
python app.py
```
## Дополнительные фичи 
1. RESTful API  
Реализовано API с использованием FastAPI , которое принимает изображение и возвращает описание.

2. Оптимизация производительности  
Реализована асинхронную обработку запросов с использованием asyncio.
3. Улучшение интерфейса   
Интерфейс немного изменен с использованием CSS.
4. Обработка ошибок   
Добавлена обработку ошибок и логирование.
5. Дополнительные функции   
Добавлена возможность сохранения истории запросов в базу данных PostgreSQL.
Реализован функционал для просмотра истории запросов через API.

http://localhost:8000/generate_caption_with_history/ - Генерирует текстовое описание для загруженного изображения и сохраняет историю запроса в базе данных.

Args: file (UploadFile): Изображение, загруженное пользователем. session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.   
Returns: dict: Словарь с ключами "id" и "description", содержащими ID созданной записи и текстовое описание изображения. В случае ошибки вызывает HTTP-исключение с кодом 500.

http://localhost:8000/histories/ - Возвращает историю всех запросов на генерацию описаний изображений.

Args: session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.   
Returns: list: Список словарей с информацией о каждой записи: - "id": ID записи. - "description": Текстовое описание изображения. - "created_at": Дата и время создания записи.

