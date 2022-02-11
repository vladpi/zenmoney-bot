from typing import TYPE_CHECKING

from aiogram import filters, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

from modules.zenmoney import get_auth_url

from ..bot import dispatcher

if TYPE_CHECKING:
    from modules.users import UserModel


@dispatcher.message_handler(filters.CommandStart(), state='*')
async def start_handler(message: types.Message, state: FSMContext, user: 'UserModel'):
    await state.finish()
    await message.answer(f'Hello, {user.first_name}!', reply_markup=ReplyKeyboardRemove())


@dispatcher.message_handler(filters.Command('login'), state='*')
async def login_handler(message: types.Message, state: FSMContext, user: 'UserModel'):
    await state.finish()
    auth_url = get_auth_url(user.id)

    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton('Авторизоваться', url=auth_url)]],
    )

    await message.answer('Login', reply_markup=reply_markup)
