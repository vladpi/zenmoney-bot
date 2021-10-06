from asyncio import gather
from typing import TYPE_CHECKING, Optional, Tuple

from core import settings
from core.clients import zenmoney_client
from modules.accounts import create_account_from_zenmoney_account
from modules.categories import create_category_from_zenmoney_tag
from modules.users import init_user_zenmoney_data

if TYPE_CHECKING:
    from modules.users import UserModel


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

    await init_user_zenmoney_data(user, token, diff.server_timestamp)

    if diff.tag is not None:
        await gather(*[create_category_from_zenmoney_tag(user.id, tag) for tag in diff.tag])

    if diff.account is not None:
        await gather(
            *[create_account_from_zenmoney_account(user.id, account) for account in diff.account]
        )
