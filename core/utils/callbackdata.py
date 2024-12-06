from aiogram.filters.callback_data import CallbackData


class ShowPosition(CallbackData, prefix='ShowPosition'):
    id: int
    shelf: int
    subject: str
    count: int
    project: str
    freebalance: int
    descr: str
