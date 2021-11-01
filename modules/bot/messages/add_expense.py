from typing import TYPE_CHECKING, List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from modules.bot import buttons

from ..bot import bot

if TYPE_CHECKING:
    from modules.accounts import AccountModel
    from modules.categories import CategoryModel


async def select_account(to_chat_id: int, accounts: List['AccountModel']):
    keyboard = [[KeyboardButton(account.title)] for account in accounts]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await bot.send_message(
        chat_id=to_chat_id,
        text='Выбери счет',
        reply_markup=reply_markup,
    )


async def add_expense_amount(to_chat_id: int):
    reply_markup = ReplyKeyboardRemove()
    await bot.send_message(
        chat_id=to_chat_id,
        text='Отправь сумму и комментарий',
        reply_markup=reply_markup,
    )


async def wrong_expense_amount(to_chat_id: int):
    reply_markup = ReplyKeyboardRemove()
    await bot.send_message(
        chat_id=to_chat_id,
        text='Не вижу сумму.\nПовтори в формате: <pre>123.45</pre>',
        reply_markup=reply_markup,
    )


async def add_expense_date(to_chat_id: int):
    keyboard = [
        [KeyboardButton(buttons.YESTERDAY), KeyboardButton(buttons.TODAY)],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await bot.send_message(
        chat_id=to_chat_id,
        text='Выбери или отправь дату',
        reply_markup=reply_markup,
    )


async def wrong_expense_date(to_chat_id: int):
    await bot.send_message(
        chat_id=to_chat_id,
        text='Не вижу даты.\nПовтори в формате: <pre>01.02.20</pre>',
    )


async def select_category(to_chat_id: int, categories: List['CategoryModel']):
    keyboard = [[KeyboardButton(category.title)] for category in categories]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await bot.send_message(
        chat_id=to_chat_id,
        text='Выбери категорию',
        reply_markup=reply_markup,
    )


# FIXME
async def expense_created(to_chat_id: int):
    await bot.send_message(
        chat_id=to_chat_id,
        text='Расход создан!',
        reply_markup=ReplyKeyboardRemove(),
    )
