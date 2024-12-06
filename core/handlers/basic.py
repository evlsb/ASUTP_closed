# Импортируем настройки подключения
from core.settings import settings
# Импортируем комманды
from core.utils.commands import set_commands
from aiogram.filters import Command
from core.handlers.add_subject import *
from core.handlers.show_subjects import *
from core.handlers.callback import ShowPosition_C


# Запуск бота
async def start():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    await set_commands(bot)

    # Регистрация хендлеров
    dp.message.register(add, Command(commands=['add']))
    dp.message.register(process_question1, Form.question1)
    dp.message.register(process_question2, Form.question2)
    dp.message.register(process_question3, Form.question3)
    dp.message.register(process_question4, Form.question4)
    dp.message.register(process_question5, Form.question5)
    dp.message.register(process_question6, Form.question6)

    # Хендлер для вывода содержимого шкафа
    dp.message.register(show_subject, Command(commands=['show']))
    # Хендлер для вывода содержимого шкафа
    dp.message.register(show_subject_inline, Command(commands=['show_inline']))

    dp.callback_query.register(ShowPosition_C, ShowPosition.filter())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

