from aiogram import Bot
from aiogram.types import ParseMode

from core import settings

bot = Bot(
    token=settings.TG_BOT_TOKEN.get_secret_value(),
    parse_mode=ParseMode.HTML,
)
