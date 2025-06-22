# handlers/settings_handler.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database import requests as rq
from keyboards import settings_keyboard, language_selection_keyboard, role_selection_keyboard
from locales.translations import get_text

router = Router()


@router.callback_query(F.data == "settings")
async def settings_handler(callback: CallbackQuery, session: AsyncSession):
    user = await rq.get_user(session, callback.from_user.id)
    lang_code = user.language_code
    await callback.message.edit_text(
        get_text('settings_prompt', lang_code),
        reply_markup=settings_keyboard(lang_code)
    )
    await callback.answer()


@router.callback_query(F.data == "change_language")
async def change_language_handler(callback: CallbackQuery):
    # Просто показываем меню выбора языка снова
    await callback.message.edit_text(
        get_text('choose_language', 'ru'),  # Это сообщение показываем на всех языках сразу
        reply_markup=language_selection_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "choose_role")
async def choose_role_handler(callback: CallbackQuery, session: AsyncSession):
    user = await rq.get_user(session, callback.from_user.id)
    lang_code = user.language_code
    await callback.message.edit_text(
        get_text('choose_role_prompt', lang_code),
        reply_markup=await role_selection_keyboard(session, lang_code)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_role_"))
async def set_role_handler(callback: CallbackQuery, session: AsyncSession):
    role_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id

    # Если role_id == 0, сбрасываем роль
    await rq.set_user_role(session, user_id, role_id if role_id != 0 else None)

    user = await rq.get_user(session, user_id)
    lang_code = user.language_code

    if role_id == 0:
        await callback.answer(get_text('role_removed_success', lang_code), show_alert=True)
    else:
        role_name = getattr(user.role, f'name_{lang_code}', user.role.name_ru)
        await callback.answer(get_text('role_set_success', lang_code).format(role_name=role_name), show_alert=True)

    # Возвращаемся в меню настроек
    await callback.message.edit_text(
        get_text('settings_prompt', lang_code),
        reply_markup=settings_keyboard(lang_code)
    )