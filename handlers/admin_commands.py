# handlers/admin_commands.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from database import requests as rq

router = Router()

# Фильтр, который пропускает только админов бота (из нашей БД)
router.message.filter(F.from_user.id.in_({5884034743}))  # <-- Вставьте сюда ID админов


@router.message(Command("add_channel"))
async def add_channel_command(message: Message, session: AsyncSession):
    """
    Добавляет канал. Формат: /add_channel ID Название Ссылка
    Пример: /add_channel -1001234567890 Мой Канал https://t.me/my_channel
    """
    try:
        parts = message.text.split(maxsplit=3)
        if len(parts) != 4:
            await message.reply("Неверный формат. Используйте:\n`/add_channel ID Название Ссылка`")
            return

        _, channel_id_str, name, url = parts
        channel_id = int(channel_id_str)

        response_text = await rq.add_channel(session, channel_id, name, url)
        await message.reply(response_text)

    except (ValueError, IndexError):
        await message.reply("Ошибка в данных. Проверьте ID канала (должно быть число) и формат команды.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")