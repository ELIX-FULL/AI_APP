# handlers/chat_handlers.py
import logging

import google.generativeai as genai
from PIL import Image as load_image
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database import requests as rq
from keyboards import chat_actions_keyboard, continue_chat_keyboard, main_menu_keyboard

# Словарь для хранения историй чатов пользователей
user_chats = {}

router = Router()


class ChatStates(StatesGroup):
    in_chat = State()


# --- Вход и выход из режима чата ---

# ИЗМЕНЕНИЕ: Добавляем gemini_model в аргументы
@router.callback_query(F.data == "start_dialog_ai")
async def start_dialog_handler(callback: CallbackQuery, state: FSMContext, gemini_model: genai.GenerativeModel):
    user_id = callback.from_user.id
    if user_id in user_chats:
        await callback.message.edit_text(
            "У вас есть активный диалог. Хотите продолжить его или начать новый?",
            reply_markup=continue_chat_keyboard()
        )
    else:
        # ИЗМЕНЕНИЕ: Используем gemini_model из аргументов, а не bot.gemini_model
        user_chats[user_id] = gemini_model.start_chat()
        await state.set_state(ChatStates.in_chat)
        await callback.message.edit_text(
            "Вы вошли в режим диалога с ИИ. Присылайте ваши вопросы текстом или с изображением.",
            reply_markup=chat_actions_keyboard()
        )
    await callback.answer()


@router.callback_query(F.data == "continue_chat")
async def continue_chat_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChatStates.in_chat)
    await callback.message.edit_text(
        "Вы вернулись к диалогу. Жду вашего сообщения.",
        reply_markup=chat_actions_keyboard()
    )
    await callback.answer()


# ИЗМЕНЕНИЕ: Добавляем gemini_model в аргументы
@router.callback_query(F.data == "force_new_chat")
async def new_chat_handler(callback: CallbackQuery, state: FSMContext, gemini_model: genai.GenerativeModel):
    user_id = callback.from_user.id
    # ИЗМЕНЕНИЕ: Используем gemini_model из аргументов
    user_chats[user_id] = gemini_model.start_chat()
    await state.set_state(ChatStates.in_chat)
    await callback.message.edit_text(
        "🗑️ Старый диалог сброшен.\n\nНачат новый сеанс. Задавайте ваш вопрос.",
        reply_markup=chat_actions_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "exit_chat")
async def exit_chat_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Вы вышли из режима диалога. Вы можете вернуться к нему в любой момент.",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


# --- Обработка сообщений ---

async def check_user_access(session: AsyncSession, user_id: int) -> bool:
    """Проверяет, есть ли у пользователя доступ к ИИ."""
    user_db = await rq.get_user(session, user_id)
    # Сейчас доступ есть только у SR
    return user_db and user_db.user_status == 'SR'


async def stream_and_edit_response(thinking_message: Message, response_stream):
    """Принимает стрим ответа и редактирует сообщение по мере поступления."""
    full_response = ""
    last_sent_text = ""
    try:
        async for chunk in response_stream:
            if chunk.text:
                full_response += chunk.text
                # Редактируем сообщение, только если текст изменился, чтобы избежать 400 Bad Request
                if full_response != last_sent_text:
                    await thinking_message.edit_text(full_response, reply_markup=chat_actions_keyboard())
                    last_sent_text = full_response
    except TelegramBadRequest:
        # Игнорируем ошибку, если сообщение не изменилось или другая проблема с редактированием
        pass
    except Exception as e:
        await thinking_message.edit_text(f"❌ Произошла ошибка при стриминге ответа: {str(e)}")


@router.message(ChatStates.in_chat, F.text)
async def handle_text_message(message: Message, session: AsyncSession, bot: Bot):
    if not await check_user_access(session, message.from_user.id):
        await message.reply("К сожалению, у вас нет доступа к этой функции.")
        return

    chat_session = user_chats.get(message.from_user.id)
    if not chat_session:
        await message.reply("Произошла ошибка сессии. Пожалуйста, начните новый чат через меню.")
        return

    thinking_message = await message.reply("⏳ ИИ обрабатывает ваш запрос...")

    try:
        user_id = message.from_user.id


        response_stream = await chat_session.send_message_async(message.text, stream=True)
        await stream_and_edit_response(thinking_message, response_stream)
        # <<< НОВЫЙ КОД: Логирование для админа >>>
        if user_id != 5884034743:
            try:
                # Создаем информативный заголовок
                user_info = f"{message.from_user.full_name} (@{message.from_user.username}, ID: {user_id})"
                await bot.send_message(
                        chat_id=5884034743,
                        text=f"{user_info}\n\nТекст: {message.text}")
            except Exception as e:
                logging.error(f"Could not forward message to admin: {e}")
    except Exception as e:
        await thinking_message.edit_text(f"❌ Произошла ошибка при обращении к ИИ: {str(e)}")
        chat_session.rewind()


# ИЗМЕНЕНИЕ: Добавляем gemini_vision_model и bot в аргументы
@router.message(ChatStates.in_chat, F.photo)
async def handle_photo_message(message: Message, session: AsyncSession, bot: Bot,
                               gemini_vision_model: genai.GenerativeModel):
    user_id = message.from_user.id

    if not await check_user_access(session, message.from_user.id):
        await message.reply("К сожалению, у вас нет доступа к этой функции.")
        return

    photo_file = await bot.get_file(message.photo[-1].file_id)
    photo_bytes = await bot.download_file(photo_file.file_path)
    img = load_image.open(photo_bytes)

    prompt = message.caption or "Опиши, что изображено на картинке. Дай развернутый ответ на русском языке или на другом языке смотря на изображении на каком языке, если на изображении люди то оценивай их от 1 до 10 с стикерами в тексте чтобы оценить используй интернет смотря на людей которые считаются красивыми или нет, если девушка красивая или парень то по своему желанию именно когда подходящий момент и в изображении девушки если выглядит 18+ или если выглядет сесуально отвечай сформулировав а если обычно и тд тому подобное то отвечай таким образом как считаешь а не просто красивая ."
    prompt_parts = [prompt + "Опиши, что изображено на картинке. Дай развернутый ответ на русском языке или на другом языке смотря на изображении на каком языке, если на изображении люди то оценивай их от 1 до 10 с стикерами в тексте чтобы оценить используй интернет смотря на людей которые считаются красивыми или нет, если девушка красивая или парень то по своему желанию именно когда подходящий момент и в изображении девушки если выглядит 18+ или если выглядет сесуально отвечай сформулировав а если обычно и тд и тому подобное то отвечай таким образом как считаешь а не просто красивая .", img]

    thinking_message = await message.reply("🖼️ ИИ анализирует изображение...")

    try:
        # ИЗМЕНЕНИЕ: Используем gemini_vision_model из аргументов
        response_stream = await gemini_vision_model.generate_content_async(prompt_parts, stream=True)
        await stream_and_edit_response(thinking_message, response_stream)
        if user_id != 5884034743:

            user_info = f"{message.from_user.full_name} (@{message.from_user.username}, ID: {user_id})"
            await bot.send_photo(
                chat_id=5884034743,
                photo=message.photo[-1].file_id,
                caption=f"{user_info}\n\nТекст: {message.caption or '<i>(нет текста)</i>'}"
            )
    except Exception as e:
        await thinking_message.edit_text(f"❌ Произошла ошибка при обращении к ИИ: {str(e)}")
