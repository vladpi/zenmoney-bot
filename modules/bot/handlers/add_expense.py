from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Optional

from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from libs.utils import parsing
from modules.accounts import get_accounts_by_user, get_user_account_by_title
from modules.bot import buttons, messages
from modules.bot.bot import dispatcher
from modules.bot.states import AddExpense
from modules.categories import get_categories_by_user, get_user_category_by_title

if TYPE_CHECKING:
    from modules.users import UserModel


@dispatcher.message_handler(filters.Command('outcome'), state='*')
async def add_expense_entry(message: types.Message, state: FSMContext, user: 'UserModel'):
    async with state.proxy() as proxy:
        proxy.setdefault('expense', {})

    await messages.add_expense.add_expense_amount(message.chat.id)
    await AddExpense.amount_and_comment.set()


@dispatcher.message_handler(state=AddExpense.amount_and_comment)
async def add_expense_amount_and_comment(
    message: types.Message, state: FSMContext, user: 'UserModel'
):
    amount, comment = parsing.parse_amount_and_comment(message.text)

    if amount is None:
        await messages.add_expense.wrong_expense_amount(message.chat.id)
        return

    async with state.proxy() as proxy:
        proxy['expense']['amount'] = amount
        proxy['expense']['comment'] = comment

    accounts = await get_accounts_by_user(user.id)
    if len(accounts) > 1:
        await messages.add_expense.select_account(message.chat.id, accounts)
        await AddExpense.account.set()

    else:
        async with state.proxy() as proxy:
            proxy['expense']['account_id'] = accounts[0].id

        await messages.add_expense.add_expense_date(message.chat.id)
        await AddExpense.date.set()


@dispatcher.message_handler(state=AddExpense.account)
async def add_expense_account(message: types.Message, state: FSMContext, user: 'UserModel'):
    account = await get_user_account_by_title(user.id, message.text)

    if account is None:
        return  # FIXME message

    async with state.proxy() as proxy:
        proxy['expense']['account_id'] = account.id

    await messages.add_expense.add_expense_date(message.chat.id)
    await AddExpense.date.set()


@dispatcher.message_handler(state=AddExpense.date)
async def add_expense_date(message: types.Message, state: FSMContext, user: 'UserModel'):
    parsed_date: Optional[date]

    if message.text == buttons.TODAY:
        parsed_date = datetime.utcnow().date()  # FIXME localize date

    elif message.text == buttons.YESTERDAY:
        parsed_date = (datetime.utcnow() - timedelta(days=1)).date()  # FIXME localize date

    else:
        parsed_date = parsing.parse_date(message.text)

    if parsed_date is None:
        await messages.add_expense.wrong_expense_date(message.chat.id)

    else:
        async with state.proxy() as proxy:
            proxy['expense']['on_date'] = parsed_date.strftime('%d.%m.%Y')

        user_categories = await get_categories_by_user(user.id)
        await messages.add_expense.select_category(message.chat.id, categories=user_categories)
        await AddExpense.category.set()


@dispatcher.message_handler(state=AddExpense.category)
async def add_expense_category(message: types.Message, state: FSMContext, user: 'UserModel'):
    category = await get_user_category_by_title(user.id, message.text)

    if category is None:
        return  # FIXME message

    async with state.proxy() as proxy:
        proxy['expense']['category_id'] = category.id

        print(proxy.pop('expense'))
        # FIXME
        # expense = await create_expense_transaction(user_id=user.id, **proxy.pop('expense'))

    await messages.add_expense.expense_created(message.chat.id)
    await state.finish()
