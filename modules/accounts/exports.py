from typing import TYPE_CHECKING, List, Optional

from .internals import create_from_zenmoney_account
from .service import account_service

if TYPE_CHECKING:
    from libs.zenmoney.schemas import Account

    from .schemas import AccountModel


async def create_account_from_zenmoney_account(user_id: int, account: 'Account') -> 'AccountModel':
    return await create_from_zenmoney_account(user_id, account)


async def get_accounts_by_user(user_id: int) -> List['AccountModel']:
    return await account_service.get_by_user(user_id)


async def get_user_account_by_title(user_id: int, title: str) -> Optional['AccountModel']:
    return await account_service.get_by_title(user_id, title)


async def delete_account(id_: str) -> None:
    return await account_service.delete(id_)


async def update_account_transactions_count(
    id_: str,
    transactions_count: Optional[int] = None,
) -> None:
    return await account_service.update_transactions_count(id_, transactions_count)
