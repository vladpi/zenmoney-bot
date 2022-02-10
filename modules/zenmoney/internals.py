import logging
from asyncio import gather
from collections import defaultdict
from datetime import date, datetime
from typing import TYPE_CHECKING, Coroutine, DefaultDict, List, Optional, Tuple
from uuid import uuid4

from core import settings
from core.clients import zenmoney_client
from libs.zenmoney.schemas import DiffResponse, Transaction
from modules.accounts import create_account_from_zenmoney_account, delete_account
from modules.categories import (
    create_category_from_zenmoney_tag,
    delete_category,
    update_category_transactions_count,
)
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
    diff = await _sync_by_diff(user_id=user.id, user_token=token)

    await gather(
        init_user_zenmoney_data(
            user=user,
            token=token,
            last_sync=diff.server_timestamp,
            user_id=diff.user[0].id,  # type: ignore
        ),
        _init_categories_transactions_count(diff),
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

    diff = await _sync_by_diff(
        user_id=user.id,
        user_token=user.zenmoney_token.decrypted,  # type: ignore
        last_sync=user.zenmoney_last_sync,  # type: ignore
        transactions=[transaction],
    )

    await gather(
        update_user_zenmoney_last_sync(user, diff.server_timestamp),
        update_category_transactions_count(category_id),
    )


async def _sync_by_diff(
    user_id: int,
    user_token: str,
    last_sync: int = 0,
    transactions: Optional[List[Transaction]] = None,
) -> DiffResponse:
    # FIXME check error
    diff = await zenmoney_client.diff(
        user_token=user_token,
        server_timestamp=last_sync,
        transaction=transactions,
    )

    await _handle_diff_changes(user_id, diff)

    return diff


async def _handle_diff_changes(user_id: int, diff: DiffResponse) -> None:
    tasks: List[Coroutine] = []

    if diff.tag is not None:
        tasks += [create_category_from_zenmoney_tag(user_id, tag) for tag in diff.tag]

    if diff.account is not None:
        tasks += [
            create_account_from_zenmoney_account(user_id, account) for account in diff.account
        ]

    if diff.deletion is not None:
        for deletion in diff.deletion:
            if deletion.object == 'tag':
                tasks.append(delete_category(deletion.id))
            elif deletion.object == 'account':
                tasks.append(delete_account(deletion.id))

    await gather(*tasks)


async def _init_categories_transactions_count(diff: DiffResponse) -> None:
    if diff.transaction is None:
        return None

    categories_transactions_count: DefaultDict[str, int] = defaultdict(int)

    for transaction in diff.transaction:
        if transaction.tag is None:
            continue

        for tag in transaction.tag:
            categories_transactions_count[tag] += 1

    await gather(
        *[
            update_category_transactions_count(id_, count)
            for id_, count in categories_transactions_count.items()
        ]
    )
