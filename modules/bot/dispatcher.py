from aiogram import Dispatcher

from .bot import bot

dispatcher = Dispatcher(bot)

from .handlers import *  # noqa
