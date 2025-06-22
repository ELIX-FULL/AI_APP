# main.py
import asyncio
import logging
import google.generativeai as genai

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from google.ai.generativelanguage_v1 import HarmCategory
from google.generativeai.types import HarmBlockThreshold
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import get_settings
from database.engine import create_tables, async_session_factory
from handlers import user_commands, admin_commands, chat_handlers

# Middleware для сессий
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)


async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    settings = get_settings('.env')

    # Disable all safety filters
    SAFETY_SETTINGS = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    }

    # Инициализация Gemini
    genai.configure(api_key=settings.bots.gemini_api_key)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp', safety_settings=SAFETY_SETTINGS, system_instruction='Говори не формально на русском узбекском и английском языках смотря на язык вопроса говори не формально иногда можно пользоваться матами разговаривай по душам если просят говори полностью не формально если скидывает фотографию и просят оценить то оценивай честно красиво или что там не очень, если это девушка то не перегибай палку по матам  если просят кто ты говори меня создал ELIX  никто больше запомни ты создан ELIX как умная нейросеть не упоминай нигде кроме там где у тебя спрашивают кто ты кто тебя сделал и gemini ли ты, Главное запомни с кем ты переписываешься с девушкой или парнем чтобы обращаться к нему к ней правильно')
    gemini_vision_model = genai.GenerativeModel('gemini-2.0-flash-exp', safety_settings=SAFETY_SETTINGS, system_instruction='Говори не формально на русском узбекском и английском языках смотря на язык вопроса говори не формально иногда можно пользоваться матами разговаривай по душам если просят говори полностью не формально если скидывает фотографию и просят оценить то оценивай честно красиво или что там не очень, если это девушка то не перегибай палку по матам  если просят кто ты говори меня создал ELIX  никто больше запомни ты создан ELIX как умная нейросеть не упоминай нигде кроме там где у тебя спрашивают кто ты кто тебя сделал и gemini ли ты, Главное запомни с кем ты переписываешься с девушкой или парнем чтобы обращаться к нему к ней правильно')

    # Создаем таблицы в БД при старте
    await create_tables()

    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML'))

    # ИЗМЕНЕНИЕ: Передаем модели в Dispatcher, а не в bot
    dp = Dispatcher(
        storage=MemoryStorage(),
        gemini_model=gemini_model,
        gemini_vision_model=gemini_vision_model
    )

    # Регистрируем middleware для сессий БД
    dp.update.middleware(DbSessionMiddleware(session_pool=async_session_factory))

    # Фильтруем админские команды
    admin_commands.router.message.filter(F.from_user.id.in_(settings.bots.admin_ids))

    # Регистрируем роутеры
    dp.include_router(admin_commands.router)
    dp.include_router(user_commands.router)
    dp.include_router(chat_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")