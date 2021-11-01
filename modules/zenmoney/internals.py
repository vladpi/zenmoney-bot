import logging
from asyncio import gather
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional, Tuple
from uuid import uuid4

from core import settings
from core.clients import zenmoney_client
from libs.zenmoney.schemas import Transaction
from modules.accounts import create_account_from_zenmoney_account
from modules.categories import create_category_from_zenmoney_tag
from modules.users import init_user_zenmoney_data, update_user_zenmoney_last_sync

if TYPE_CHECKING:
    from modules.users import UserModel


logger = logging.getLogger(__name__)


def get_auth_url(user_id: int) -> str:
    redirect_url = f'{settings.WEBHOOK_HOST}/zenmoney/auth/{user_id}'
    return zenmoney_client.get_auth_url(redirect_url)


async def get_auth_tokens(code: str, user_id: int) -> Tuple[Optional[str], Optional[str]]:
    redirect_url = f'{settings.WEBHOOK_HOST}/zenmoney/auth/{user_id}'

    response = await zenmoney_client.get_token(code, redirect_url)

    return response.access_token, response.refresh_token


async def init_user(user: 'UserModel', token: str):
    diff = await zenmoney_client.diff(token, server_timestamp=0)

    # FIXME check error

    await init_user_zenmoney_data(
        user=user,
        token=token,
        last_sync=diff.server_timestamp,
        user_id=diff.user[0].id,  # type: ignore
    )

    if diff.tag is not None:
        await gather(*[create_category_from_zenmoney_tag(user.id, tag) for tag in diff.tag])

    if diff.account is not None:
        await gather(
            *[create_account_from_zenmoney_account(user.id, account) for account in diff.account]
        )


async def create_expense(
    user: 'UserModel',
    amount: float,
    account_id: str,
    instrument_id: int,
    category_id: str,
    at_date: date,
    comment: Optional[str] = None,
):
    transaction = Transaction(
        id=str(uuid4()),
        changed=datetime.utcnow(),
        created=datetime.utcnow(),
        user=user.zenmoney_user_id,
        deleted=False,
        income_instrument=instrument_id,
        income_account=account_id,
        income=0,
        outcome_instrument=instrument_id,
        outcome_account=account_id,
        outcome=amount,
        tag=[category_id],
        comment=comment,
        at_date=at_date,
    )

    diff = await zenmoney_client.diff(
        user_token=user.zenmoney_token.decrypted,  # type: ignore
        server_timestamp=user.zenmoney_last_sync,  # type: ignore
        transaction=[transaction],
    )

    # FIXME check error

    await update_user_zenmoney_last_sync(user, diff.server_timestamp)
