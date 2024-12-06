from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='add',
            description='Положить'
        ),
        BotCommand(
            command='remove',
            description='Забрать'
        ),
        BotCommand(
            command='show',
            description='Показать'
        ),
        BotCommand(
            command='show_inline',
            description='Показать кнопки'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())