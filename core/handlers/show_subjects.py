import asyncpg
from aiogram import Bot, Dispatcher, types
from tabulate import tabulate
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import ShowPosition


async def create_pool():
    return await asyncpg.create_pool(user='postgres', password='Fjcm()3472', database='users', host='127.0.0.1', port=5432, command_timeout=60)


# Хендлер для вывода содержимого шкафа
async def show_subject(message: types.Message):
    pool = await create_pool()
    async with pool.acquire() as conn:
        # Запрашиваем данные из базы данных
        rows = await conn.fetch("SELECT id, shelf, subject, count, project, freebalance, descr FROM user_data")

        # Если данные существуют
        if rows:
            # Формируем таблицу в HTML формате
            table = "<b>Данные:</b>\n"
            table += "<pre>\n"
            for row in rows:
                table += f"ID: {row['id']}\nПолка: {row['shelf']}\nПредмет: {row['subject']}\nКол-во: {row['count']}\nПроект: {row['project']}\n"
                table += "-----------------------\n"
            table += "</pre>"

            # Отправляем таблицу в HTML формате
            await message.answer(table, parse_mode="HTML")
        else:
            await message.answer("Данные отсутствуют.")


# Хендлер для вывода содержимого шкафа (Inline)
async def show_subject_inline(message: types.Message):
    pool = await create_pool()
    async with pool.acquire() as conn:
        # Запрашиваем данные из базы данных
        rows = await conn.fetch("SELECT id, shelf, subject, count, project, freebalance, descr FROM user_data")

        # Если данные существуют
        if rows:
            keyboard_builder = InlineKeyboardBuilder()
            for row in rows:
                # Создаём кнопку для каждого проекта
                #button_text = f"ID: {row['id']}, Полка: {row['shelf']}, Проект: {row['project']}"
                keyboard_builder.button(text=row['subject'], callback_data=ShowPosition(id=row['id'], shelf=row['shelf'], subject=row['subject'], count=row['count'], project=row['project'], freebalance=row['freebalance'], descr=row['descr']))

            keyboard_builder.adjust(1)
            k = keyboard_builder.as_markup()

            # Отправляем клавиатуру пользователю
            await message.answer("Выберите проект:", reply_markup=k)

        else:
            await message.answer("Данные отсутствуют.")