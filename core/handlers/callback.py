from aiogram import Bot
from aiogram.types import CallbackQuery
from core.utils.callbackdata import ShowPosition


async def ShowPosition_C(call: CallbackQuery, bot: Bot, callback_data: ShowPosition):
    id = callback_data.id
    shelf = callback_data.shelf
    subject = callback_data.subject
    count = callback_data.count
    project = callback_data.project
    freebalance = callback_data.freebalance
    descr = callback_data.descr
    answer = f'Выбран: id={id} полка: {shelf} предмет: {subject} кол-во: {count} проект: {project} остаток: {freebalance} описание: {descr}'
    await call.message.answer(answer)
    await call.answer()