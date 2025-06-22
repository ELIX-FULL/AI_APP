# locales/translations.py

texts = {
    'choose_language': {
        'ru': "🇷🇺 Пожалуйста, выберите язык:",
        'en': "🇬🇧 Please select a language:",
        'uz': "🇺🇿 Iltimos, tilni tanlang:",
    },
    'welcome': {
        'ru': "<b>👋 Приветствую, {name}!</b>\n\nВыберите действие в меню:",
        'en': "<b>👋 Greetings, {name}!</b>\n\nChoose an action from the menu:",
        'uz': "<b>👋 Assalomu alaykum, {name}!</b>\n\nMenyudan amalni tanlang:",
    },
    'subscribe_prompt': {
        'ru': "<b>👋 Приветствую, {name}!</b>\n\n<i>👇 Для использования бота, подпишитесь на каналы:</i>",
        'en': "<b>👋 Greetings, {name}!</b>\n\n<i>👇 To use the bot, please subscribe to the channels:</i>",
        'uz': "<b>👋 Assalomu alaykum, {name}!</b>\n\n<i>👇 Botdan foydalanish uchun, iltimos, kanallarga obuna bo'ling:</i>",
    },
    'subscribe_success': {
        'ru': "✅ Вы успешно подписались!",
        'en': "✅ You have successfully subscribed!",
        'uz': "✅ Siz muvaffaqiyatli obuna bo'ldingiz!",
    },
    'subscribe_fail': {
        'ru': "❌ Вы не подписались на все каналы.",
        'en': "❌ You are not subscribed to all channels.",
        'uz': "❌ Siz barcha kanallarga obuna bo'lmagansiz.",
    },
    'main_menu_prompt': {
        'ru': "<b>👋 Отлично, {name}!</b>\n\nТеперь вам доступны все функции.",
        'en': "<b>👋 Great, {name}!</b>\n\nAll features are now available to you.",
        'uz': "<b>👋 Ajoyib, {name}!</b>\n\nEndi barcha funksiyalar siz uchun mavjud.",
    },
    # Кнопки
    'btn_ask_ai': {'ru': "🤖 Задать вопрос ИИ", 'en': "🤖 Ask AI", 'uz': "🤖 Sun'iy intellektga savol bering"},
    'btn_profile': {'ru': "👤 Мой профиль", 'en': "👤 My Profile", 'uz': "👤 Mening profilim"},
    'btn_settings': {'ru': "⚙️ Настройки", 'en': "⚙️ Settings", 'uz': "⚙️ Sozlamalar"},
    'btn_back': {'ru': "⬅️ Назад", 'en': "⬅️ Back", 'uz': "⬅️ Orqaga"},
    'btn_change_lang': {'ru': "🌐 Сменить язык", 'en': "🌐 Change Language", 'uz': "🌐 Tilni o'zgartirish"},
    'btn_choose_role': {'ru': "🎭 Выбрать роль ИИ", 'en': "🎭 Choose AI Role", 'uz': "🎭 AI rolini tanlang"},
    'btn_remove_role': {'ru': "🗑️ Убрать роль", 'en': "🗑️ Remove Role", 'uz': "🗑️ Rolni olib tashlash"},
    # Профиль и настройки
    'profile_text': {
        'ru': "👤 <b>Ваш профиль:</b>\n\n<b>ID:</b> <code>{user_id}</code>\n<b>Язык:</b> {lang}\n<b>Текущая роль ИИ:</b> {role}",
        'en': "👤 <b>Your Profile:</b>\n\n<b>ID:</b> <code>{user_id}</code>\n<b>Language:</b> {lang}\n<b>Current AI Role:</b> {role}",
        'uz': "👤 <b>Sizning profilingiz:</b>\n\n<b>ID:</b> <code>{user_id}</code>\n<b>Til:</b> {lang}\n<b>Joriy AI roli:</b> {role}",
    },
    'no_role': {'ru': "Не выбрана", 'en': "Not selected", 'uz': "Tanlanmagan"},
    'settings_prompt': {'ru': "⚙️ Меню настроек", 'en': "⚙️ Settings Menu", 'uz': "⚙️ Sozlamalar menyusi"},
    'choose_role_prompt': {'ru': "🎭 Выберите роль для ИИ:", 'en': "🎭 Choose a role for the AI:",
                           'uz': "🎭 AI uchun rolni tanlang:"},
    'role_set_success': {
        'ru': "✅ Роль '{role_name}' успешно установлена!",
        'en': "✅ Role '{role_name}' has been set successfully!",
        'uz': "✅ '{role_name}' roli muvaffaqiyatli o'rnatildi!",
    },
    'role_removed_success': {
        'ru': "✅ Роль успешно убрана.",
        'en': "✅ Role removed successfully.",
        'uz': "✅ Rol muvaffaqiyatli olib tashlandi.",
    },
    # Логика чата
    'chat_enter': {
        'ru': "Вы вошли в режим диалога с ИИ. Присылайте ваши вопросы текстом или с изображением.",
        'en': "You have entered AI chat mode. Send your questions as text or with an image.",
        'uz': "Siz sun'iy intellekt bilan muloqot rejimiga kirdingiz. Savollaringizni matn yoki rasm bilan yuboring."
    },
    'btn_new_chat': {'ru': "🗑️ Начать новый чат", 'en': "🗑️ Start New Chat", 'uz': "🗑️ Yangi suhbat boshlash"},
    'btn_exit_chat': {'ru': "🚪 Выйти из чата", 'en': "🚪 Exit Chat", 'uz': "🚪 Suhbatdan chiqish"},
    'chat_in_progress_warning': {
        'ru': "Вы находитесь в режиме диалога с ИИ. 🤖\n\nЧтобы выйти из него и использовать другие команды, воспользуйтесь кнопками ниже.",
        'en': "You are in AI chat mode. 🤖\n\nTo exit and use other commands, please use the buttons below.",
        'uz': "Siz sun'iy intellekt bilan muloqot rejimidasiz. 🤖\n\nBoshqa buyruqlardan foydalanish uchun undan chiqish uchun quyidagi tugmalardan foydalaning."
    },
    'continue_chat_prompt': {
        'ru': "У вас есть активный диалог. Хотите продолжить его или начать новый?",
        'en': "You have an active chat. Do you want to continue it or start a new one?",
        'uz': "Sizda faol suhbat mavjud. Uni davom ettirishni yoki yangisini boshlashni xohlaysizmi?",
    },
    'return_to_chat_prompt': {
        'ru': "Вы вернулись к диалогу. Жду вашего сообщения.",
        'en': "You have returned to the chat. Awaiting your message.",
        'uz': "Siz suhbatga qaytdingiz. Xabaringizni kutyapman.",
    },
    'new_chat_forced': {
        'ru': "🗑️ Старый диалог сброшен.\n\nНачат новый сеанс. Задавайте ваш вопрос.",
        'en': "🗑️ Old chat has been reset.\n\nA new session has started. Ask your question.",
        'uz': "🗑️ Eski suhbat tiklandi.\n\nYangi sessiya boshlandi. Savolingizni bering.",
    },
    'exit_chat_message': {
        'ru': "Вы вышли из режима диалога. Вы можете вернуться к нему в любой момент.",
        'en': "You have exited the chat mode. You can return to it at any time.",
        'uz': "Siz suhbat rejimidan chiqdingiz. Unga istalgan vaqtda qaytishingiz mumkin.",
    },
    'no_access': {
        'ru': "К сожалению, у вас нет доступа к этой функции.",
        'en': "Unfortunately, you do not have access to this feature.",
        'uz': "Afsuski, sizda bu funksiyaga kirish huquqi yo'q.",
    },
    'session_error': {
        'ru': "Произошла ошибка сессии. Пожалуйста, начните новый чат через меню.",
        'en': "A session error occurred. Please start a new chat from the menu.",
        'uz': "Sessiya xatosi yuz berdi. Iltimos, menyudan yangi suhbat boshlang.",
    },

}


def get_text(key, lang='ru'):
    """Возвращает текст по ключу и языку. Если перевод отсутствует, возвращает на русском."""
    return texts.get(key, {}).get(lang, texts.get(key, {}).get('ru', ''))

