from datetime import date
from typing import TYPE_CHECKING, Optional

from . import internals

if TYPE_CHECKING:
    from modules.users import UserModel


def get_auth_url(user_id: int) -> str:
    return internals.get_auth_url(user_id)


async def create_expense_transaction(
    user: 'UserModel',
    amount: float,
    account_id: str,
    instrument_id: int,
    category_id: str,
    at_date: date,
    comment: Optional[str] = None,
):
    return await internals.create_expense(
        user=user,
        amount=amount,
        account_id=account_id,
        instrument_id=instrument_id,
        category_id=category_id,
        at_date=at_date,
        comment=comment,
    )
