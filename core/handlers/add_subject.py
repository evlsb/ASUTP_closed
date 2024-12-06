from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types
import asyncpg


async def create_pool():
    return await asyncpg.create_pool(user='postgres', password='Fjcm()3472', database='users', host='127.0.0.1', port=5432, command_timeout=60)



# Определяем класс состояний
class Form(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    question6 = State()


# Хендлер для команды /start, который начинает опрос
async def add(message: types.Message, state: FSMContext):
    await message.answer("На какую полку положить?")
    await state.set_state(Form.question1)


# Хендлер для первого вопроса
async def process_question1(message: types.Message, state: FSMContext):
    # Проверяем, что ввели именно число
    if not message.text.isdigit():
        # Если не число, выводим сообщение об ошибке и просим ввести снова
        await message.answer("Ошибка: Пожалуйста, введите целое число.")
        return  # Возвращаемся, чтобы не переходить к следующему вопросу

    # Если введено число, сохраняем его как целое число
    await state.update_data(shelf=int(message.text))

    # Переходим к следующему вопросу
    await message.answer("Что за предмет (полное описание)?")
    await state.set_state(Form.question2)


# Хендлер для второго вопроса
async def process_question2(message: types.Message, state: FSMContext):
    # Сохраняем ответ на второй вопрос
    await state.update_data(subject=message.text)

    # Переходим к следующему вопросу
    await message.answer("Какое кол-во?")
    await state.set_state(Form.question3)


# Хендлер для третьего вопроса
async def process_question3(message: types.Message, state: FSMContext):
    # Проверяем, что ввели именно число
    if not message.text.isdigit():
        # Если не число, выводим сообщение об ошибке и просим ввести снова
        await message.answer("Ошибка: Пожалуйста, введите целое число.")
        return  # Возвращаемся, чтобы не переходить к следующему вопросу

    # Если введено число, сохраняем его как целое число
    await state.update_data(count=int(message.text))

    # Переходим к следующему вопросу
    await message.answer("Какой проект?")
    await state.set_state(Form.question4)


# Хендлер для четвертого вопроса
async def process_question4(message: types.Message, state: FSMContext):
    # Сохраняем ответ на третий вопрос
    await state.update_data(project=message.text)

    # Переходим к следующему вопросу
    await message.answer("Свободный остаток (1-да, 0-нет)")
    await state.set_state(Form.question5)


# Хендлер для пятого вопроса
async def process_question5(message: types.Message, state: FSMContext):
    # Проверяем, что ввели именно число
    if not message.text.isdigit():
        # Если не число, выводим сообщение об ошибке и просим ввести снова
        await message.answer("Ошибка: Пожалуйста, введите целое число.")
        return  # Возвращаемся, чтобы не переходить к следующему вопросу

    # Если введено число, сохраняем его как целое число
    await state.update_data(freebalance=int(message.text))

    # Переходим к следующему вопросу
    await message.answer("Если нужно, добавь примечание")
    await state.set_state(Form.question6)


# Хендлер для шестого вопроса
async def process_question6(message: types.Message, state: FSMContext):
    # Сохраняем ответ на третий вопрос
    await state.update_data(descr=message.text)

    # Получаем данные, которые мы собирали
    user_data = await state.get_data()

    # Формируем сообщение для вывода
    result_message = (
        f"Вот что ты положил:\n"
        f"Полка: {user_data['shelf']}\n"
        f"Предмет: {user_data['subject']}\n"
        f"Кол-во: {user_data['count']}\n"
        f"Проект: {user_data['project']}\n"
        f"Свободный остаток: {user_data['freebalance']}\n"
        f"Описание: {user_data['descr']}"
    )

    # Сохраняем данные в базе данных
    pool = await create_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            'INSERT INTO user_data (shelf, subject, count, project, freebalance, descr) VALUES ($1, $2, $3, $4, $5, $6)',
            user_data['shelf'], user_data['subject'], user_data['count'], user_data['project'], user_data['freebalance'], user_data['descr']
        )

    # Выводим результат пользователю
    await message.answer(result_message, reply_markup=ReplyKeyboardRemove())

    # Завершаем состояние
    await state.clear()






