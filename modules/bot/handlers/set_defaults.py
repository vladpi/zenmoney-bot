from typing import TYPE_CHECKING

from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from modules.accounts import get_accounts_by_user, get_user_account_by_title
from modules.bot import buttons, messages
from modules.bot.bot import dispatcher
from modules.bot.states import SetDefaultOutcomeAccount
from modules.users import update_user_default_outcome_account

if TYPE_CHECKING:
    from modules.users import UserModel


@dispatcher.message_handler(filters.Command('default_outcome_account'), state='*')
async def default_outcome_account_entry(
    message: types.Message,
    state: FSMContext,
    user: 'UserModel',
):
    accounts = await get_accounts_by_user(user.id)
    await messages.set_defaults.select_default_outcome_account(
        message.chat.id, accounts, user.default_outcome_account_id
    )
    await SetDefaultOutcomeAccount.account.set()


@dispatcher.message_handler(
    filters.Text(buttons.DELETE_DEFAULT_ACCOUNT),
    state=SetDefaultOutcomeAccount.account,
)
async def delete_default_outcome_acount(
    message: types.Message,
    state: FSMContext,
    user: 'UserModel',
):
    await update_user_default_outcome_account(user, None)

    await messages.set_defaults.default_outcome_account_saved(message.chat.id)
    await state.finish()


@dispatcher.message_handler(state=SetDefaultOutcomeAccount.account)
async def set_default_outcome_acount(message: types.Message, state: FSMContext, user: 'UserModel'):
    account = await get_user_account_by_title(user.id, message.text)

    if account is None:
        return  # FIXME message

    await update_user_default_outcome_account(user, account.id)

    await messages.set_defaults.default_outcome_account_saved(message.chat.id, account)
    await state.finish()
