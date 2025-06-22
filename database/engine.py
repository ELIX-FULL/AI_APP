# database/engine.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .models import Base

# Путь к файлу базы данных
db_file = 'database.db'
# DATABASE_URL = f"sqlite+aiosqlite:///{db_file}"
# Для продакшена лучше использовать PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")


# Создаем асинхронный "движок" для работы с БД
engine = create_async_engine(DATABASE_URL, echo=False)

# Создаем фабрику сессий, через которую будем делать запросы
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    """Функция для создания таблиц в БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    """Функция для получения сессии"""
    async with async_session_factory() as session:
        yield session