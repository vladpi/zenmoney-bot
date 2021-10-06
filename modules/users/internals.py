from typing import TYPE_CHECKING

from .schemas import EncryptedStr
from .service import user_service

if TYPE_CHECKING:
    from .schemas import UserModel


async def init_zenmoney_data(
    user: 'UserModel',
    token: str,
    last_sync: int,
) -> 'UserModel':
    user.zenmoney_token = EncryptedStr.encrypt(token)
    user.zenmoney_last_sync = last_sync
    return await user_service.put(user)


async def update_zenmoney_last_sync(user: 'UserModel', last_sync: int) -> 'UserModel':
    user.zenmoney_last_sync = last_sync
    return await user_service.put(user)
