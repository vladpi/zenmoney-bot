from typing import TYPE_CHECKING

from aiogram import filters, types

from ..bot import dispatcher

if TYPE_CHECKING:
    from modules.users import UserModel


@dispatcher.message_handler(filters.CommandStart(), state='*')
async def start_handler(message: types.Message, user: 'UserModel'):
    await message.answer(f'Hello, {user.first_name}!')
