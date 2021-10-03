from aiogram import filters, types

from ..dispatcher import dispatcher


@dispatcher.message_handler(filters.CommandStart(), state='*')
async def start_handler(message: types.Message):
    await message.answer('Hello!')
