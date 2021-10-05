from typing import Optional, Tuple

from core import settings
from core.clients import zenmoney_client


def get_auth_url(user_id: int) -> str:
    redirect_url = f'{settings.WEBHOOK_HOST}/zenmoney/auth/{user_id}'
    return zenmoney_client.get_auth_url(redirect_url)


async def get_auth_tokens(code: str, user_id: int) -> Tuple[Optional[str], Optional[str]]:
    redirect_url = f'{settings.WEBHOOK_HOST}/zenmoney/auth/{user_id}'

    response = await zenmoney_client.get_token(code, redirect_url)

    return response.access_token, response.refresh_token
