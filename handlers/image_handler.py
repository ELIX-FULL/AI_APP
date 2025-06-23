# handlers/image_handler.py

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import main_menu_keyboard
from services.image_generator import Text2ImageAPI

router = Router()


class ImageGenStates(StatesGroup):
    waiting_for_prompt = State()


@router.callback_query(F.data == "generate_image")
async def start_image_generation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ImageGenStates.waiting_for_prompt)
    await callback.message.edit_text(
        "Отправьте мне текстовое описание (промпт) того, что вы хотите создать.\n\n"
        "Например: `рыжий кот в очках читает книгу в библиотеке, высокое качество, 4k`"
    )
    await callback.answer()


@router.message(ImageGenStates.waiting_for_prompt, F.text)
async def process_image_prompt(message: Message, state: FSMContext, bot: Bot, image_api: Text2ImageAPI,
                               session: AsyncSession):
    await state.clear()
    prompt = message.text
    waiting_msg = await message.reply("🎨 Принял ваш запрос. Начинаю творить... Это может занять около минуты.")

    try:
        # ИЗМЕНЕНИЕ 4: Вызываем get_pipeline вместо get_model
        pipeline_id = await image_api.get_pipeline()
        if not pipeline_id:
            await waiting_msg.edit_text("❌ Не удалось получить пайплайн для генерации. Попробуйте позже.")
            return

        # Передаем pipeline_id в generate
        uuid = await image_api.generate(prompt, pipeline_id)
        if not uuid:
            await waiting_msg.edit_text("❌ Не удалось запустить генерацию изображения. Попробуйте позже.")
            return

        image_bytes = await image_api.check_generation(uuid)

        if image_bytes:
            await waiting_msg.delete()
            await message.reply_photo(
                photo=BufferedInputFile(image_bytes, filename="generated_image.png"),
                caption=f"✅ Ваше изображение по запросу:\n\n`{prompt}`"
            )
        else:
            await waiting_msg.edit_text(
                "❌ Не удалось сгенерировать изображение. Попробуйте другой запрос или повторите попытку позже.")

    except Exception as e:
        await waiting_msg.edit_text(f"❌ Произошла непредвиденная ошибка: {e}")


# ... (остальной код хендлера без изменений) ...
@router.message(ImageGenStates.waiting_for_prompt)
async def incorrect_input_for_image(message: Message):
    await message.reply(
        "Пожалуйста, отправьте текстовое описание для генерации изображения, или вернитесь в главное меню.")
