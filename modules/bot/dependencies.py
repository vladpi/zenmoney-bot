from aiogram import Bot, Dispatcher

from .bot import bot
from .dispatcher import dispatcher


async def get_bot_dispatcher() -> Dispatcher:
    Bot.set_current(bot)
    Dispatcher.set_current(dispatcher)
    return dispatcher
