# handlers/user_commands.py
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.exceptions import TelegramBadRequest

from database import requests as rq
from handlers.chat_handlers import ChatStates
from keyboards import channels_keyboard, main_menu_keyboard, chat_actions_keyboard

router = Router()

async def check_user_subscription(bot: Bot, user_id: int, session: AsyncSession) -> bool:
    channels = await rq.get_active_channels(session)
    if not channels:
        return True
    for channel in channels:
        try:
            member = await bot.get_chat_member(chat_id=channel.channel_id, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except TelegramBadRequest:
            return False
    return True


# --- Измененный хендлер /start ---

@router.message(CommandStart())
async def handle_start(message: Message, session: AsyncSession, bot: Bot, state: FSMContext):
    # <<< ИЗМЕНЕНИЕ: Добавили state в аргументы
    current_state = await state.get_state()

    # <<< ИЗМЕНЕНИЕ: Проверяем, не находится ли пользователь уже в чате
    if current_state == ChatStates.in_chat:
        await message.reply(
            "Вы уже находитесь в режиме диалога с ИИ. 🤖\n\n"
            "Чтобы перезапустить бота, сначала выйдите из чата с помощью кнопок ниже.",
            reply_markup=chat_actions_keyboard()
        )
        return # Прерываем выполнение функции

    # Остальная логика остается прежней, если пользователь НЕ в чате
    user = message.from_user
    name = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    await rq.add_user(session, user.id, user.username, user.full_name)

    is_subscribed = await check_user_subscription(bot, user.id, session)
    if is_subscribed:
        await message.answer(
            f"<b>👋 Приветствую, {name}!</b>\n\nВыберите действие в меню:",
            reply_markup=main_menu_keyboard(),
            parse_mode='HTML'
        )
    else:
        await message.answer(
            f"<b>👋 Приветствую, {name}!</b>\n\n<i>👇 Для использования бота, подпишитесь на каналы:</i>",
            reply_markup=await channels_keyboard(session),
            parse_mode='HTML'
        )

@router.callback_query(lambda c: c.data == "check_subscription")
async def handle_check_subscription(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    user = callback.from_user
    name = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    is_subscribed = await check_user_subscription(bot, user.id, session)
    if is_subscribed:
        await callback.answer("✅ Вы успешно подписались!", show_alert=False)
        await callback.message.edit_text(
            f"<b>👋 Отлично, {name}!</b>\n\nТеперь вам доступны все функции.",
            reply_markup=main_menu_keyboard(),
            parse_mode='HTML'
        )
    else:
        await callback.answer("❌ Вы не подписались на все каналы.", show_alert=True)

@router.callback_query(F.data == "my_profile")
async def my_profile_handler(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    current_state = await state.get_state()
    if current_state == ChatStates.in_chat:
        await callback.answer("Эта функция недоступна в режиме чата.", show_alert=True)
        return

    user_db = await rq.get_user(session, callback.from_user.id)
    if user_db:
        profile_text = (
            f"👤 <b>Ваш профиль:</b>\n\n"
            f"<b>🆔ID:</b> <code>{user_db.id}</code>\n"
            f"<b>🌟Статус:</b> {user_db.user_status}\n"
            f"<b>💰Баланс:</b> {user_db.balance} запросов (для будущих версий)\n"
            f"<b>📊Дата регистрации:</b> {user_db.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
        await callback.message.edit_text(profile_text, reply_markup=main_menu_keyboard())
    else:
        await callback.answer("Не удалось найти ваш профиль, попробуйте перезапустить бота /start", show_alert=True)

    await callback.answer()
