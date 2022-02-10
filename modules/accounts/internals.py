from typing import TYPE_CHECKING

from .schemas import AccountModel
from .service import account_service

if TYPE_CHECKING:
    from libs.zenmoney.schemas import Account


async def create_from_zenmoney_account(user_id: int, zenmoney_account: 'Account') -> AccountModel:
    account = AccountModel(
        id=zenmoney_account.id,
        user_id=user_id,
        instrument_id=zenmoney_account.instrument,
        title=zenmoney_account.title,
    )
    return await account_service.put(account, exclude_from_update={'transactions_count'})
