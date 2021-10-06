from typing import TYPE_CHECKING

from .internals import create_from_zenmoney_account

if TYPE_CHECKING:
    from libs.zenmoney.schemas import Account

    from .schemas import AccountModel


async def create_account_from_zenmoney_account(user_id: int, account: 'Account') -> 'AccountModel':
    return await create_from_zenmoney_account(user_id, account)
