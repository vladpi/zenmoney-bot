import logging

from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import Response

from modules.bot.bot import bot
from modules.users import get_user

from .internals import get_auth_tokens, init_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/zenmoney')


@router.get('/auth/{user_id:int}')
async def handle_webhook(request: Request, user_id: int, code: str) -> Response:
    logger.info(f'{user_id=} {code=} {request.url=} {request.base_url=}')

    user = await get_user(user_id)
    if user is None:
        logger.info(f'User with id={user_id} not found')
        return Response(status_code=status.HTTP_200_OK)

    access_token, _ = await get_auth_tokens(code, user_id)

    # FIXME for bot export methods
    if access_token is not None:
        await init_user(user, access_token)
        await bot.send_message(chat_id=user_id, text='Успешная авторизация в ДзенМани')
    else:
        await bot.send_message(
            chat_id=user_id,
            text='При авторизации в ДзенМани что-то пошло не так',
        )

    return Response(status_code=status.HTTP_200_OK)
