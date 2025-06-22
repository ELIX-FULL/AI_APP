# database/requests.py
from datetime import date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, Channel, UserAction


# --- Пользователи ---

async def get_user(session: AsyncSession, user_id: int):
    """Получение пользователя по его ID"""
    return await session.get(User, user_id)


async def add_user(session: AsyncSession, user_id: int, username: str, full_name: str):
    """Добавление нового пользователя"""
    # Проверяем, существует ли пользователь
    user = await get_user(session, user_id)
    if not user:
        new_user = User(id=user_id, username=username, full_name=full_name)
        session.add(new_user)
        await session.commit()
        return new_user
    return user


async def is_admin(session: AsyncSession, user_id: int) -> bool:
    """Проверка, является ли пользователь админом"""
    user = await get_user(session, user_id)
    return user.is_admin if user else False


# --- Каналы ---

async def add_channel(session: AsyncSession, channel_id: int, name: str, url: str):
    """Добавление нового канала для подписки"""
    # Проверка, существует ли уже канал с таким ID
    query = select(Channel).where(Channel.channel_id == channel_id)
    result = await session.execute(query)
    if result.scalar_one_or_none() is None:
        new_channel = Channel(channel_id=channel_id, name=name, url=url)
        session.add(new_channel)
        await session.commit()
        return f"✅ Канал '{name}' ({channel_id}) успешно добавлен."
    return f"ℹ️ Канал с ID {channel_id} уже существует."


async def get_active_channels(session: AsyncSession):
    """Получение списка всех активных каналов для проверки подписки"""
    query = select(Channel).where(Channel.active == True)
    result = await session.execute(query)
    return result.scalars().all()


# --- Активность и статистика (переписанные функции) ---

async def be_active(session: AsyncSession, user_id: int, action: str):
    """Запись действия пользователя, если он не был активен сегодня."""
    # Проверяем, было ли действие сегодня
    today = date.today()
    query = select(UserAction).where(
        UserAction.user_id == user_id,
        func.date(UserAction.timestamp) == today
    )
    result = await session.execute(query)

    if result.scalar_one_or_none() is None:
        # Если действий сегодня не было, добавляем новое
        new_action = UserAction(user_id=user_id, action=action)
        session.add(new_action)
        await session.commit()
        return True
    return False


async def get_daily_stats(session: AsyncSession):
    """Получение статистики уникальных пользователей за сегодня"""
    today = date.today()
    query = select(func.count(func.distinct(UserAction.user_id))).where(func.date(UserAction.timestamp) == today)
    result = await session.execute(query)
    return result.scalar_one()


async def get_monthly_stats(session: AsyncSession):
    """Получение статистики уникальных пользователей за текущий месяц"""
    current_month_start = date.today().replace(day=1)
    query = select(func.count(func.distinct(UserAction.user_id))).where(
        UserAction.timestamp >= current_month_start
    )
    result = await session.execute(query)
    return result.scalar_one()
