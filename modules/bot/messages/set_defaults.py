from typing import TYPE_CHECKING, List, Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from modules.bot import buttons

from ..bot import bot

if TYPE_CHECKING:
    from modules.accounts import AccountModel


async def select_default_outcome_account(
    to_chat_id: int,
    accounts: List['AccountModel'],
    default_outcome_account: Optional[str],
):
    keyboard = [[KeyboardButton(account.title)] for account in accounts]
    if default_outcome_account is not None:
        keyboard = [[KeyboardButton(buttons.DELETE_DEFAULT_ACCOUNT)]] + keyboard

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await bot.send_message(
        chat_id=to_chat_id,
        text='Выбери счет по-умолчанию для расходов',
        reply_markup=reply_markup,
    )


async def default_outcome_account_saved(to_chat_id: int, account: Optional['AccountModel'] = None):
    prefix = account.title if account is not None else 'удалён'

    await bot.send_message(
        chat_id=to_chat_id,
        text=f'Счет по-умолчанию для расходов – {prefix}',
        reply_markup=ReplyKeyboardRemove(),
    )
