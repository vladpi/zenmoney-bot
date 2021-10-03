from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from core import settings

from .middlewares import UserMiddleware

bot = Bot(
    token=settings.TG_BOT_TOKEN.get_secret_value(),
    parse_mode=ParseMode.HTML,
)

dispatcher: Dispatcher = Dispatcher(bot)
dispatcher.setup_middleware(UserMiddleware())

from .handlers import *  # noqa
