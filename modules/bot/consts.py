from aiogram.types import BotCommand

COMMANDS = [
    BotCommand('/start', 'Старт'),
    BotCommand('/outcome', 'Расход'),
    BotCommand('/login', 'Авторизоваться в ДзенМани'),
    BotCommand('/default_outcome_account', 'Установить счет для расходов'),
]
