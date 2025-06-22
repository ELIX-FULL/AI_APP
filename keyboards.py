# keyboards.py
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_keyboard():
    """Клавиатура главного меню."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="👤 Мой профиль", callback_data="my_profile"))
    builder.row(InlineKeyboardButton(text="🤖 Задать вопрос ИИ", callback_data="start_dialog_ai"))
    return builder.as_markup()

def chat_actions_keyboard():
    """Клавиатура, когда пользователь уже находится в режиме чата."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🗑️ Начать новый чат", callback_data="force_new_chat"))
    builder.row(InlineKeyboardButton(text="🚪 Выйти из чата", callback_data="exit_chat"))
    return builder.as_markup()

def continue_chat_keyboard():
    """Клавиатура, если у пользователя есть незаконченный диалог."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="➡️ Продолжить прошлый чат", callback_data="continue_chat"))
    builder.row(InlineKeyboardButton(text="🗑️ Начать новый чат", callback_data="force_new_chat"))
    return builder.as_markup()

# Функцию для каналов подписки оставим здесь же
async def channels_keyboard(session):
    from database.requests import get_active_channels
    builder = InlineKeyboardBuilder()
    channels = await get_active_channels(session)
    for channel in channels:
        builder.row(InlineKeyboardButton(text=f"➡️ {channel.name}", url=channel.url))
    builder.row(InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subscription"))
    return builder.as_markup()