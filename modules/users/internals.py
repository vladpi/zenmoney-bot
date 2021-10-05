from typing import TYPE_CHECKING

from .schemas import EncryptedStr
from .service import user_service

if TYPE_CHECKING:
    from .schemas import UserModel


async def update_zenmoney_token(user: 'UserModel', token: str) -> 'UserModel':
    user.zenmoney_token = EncryptedStr.encrypt(token)
    return await user_service.put(user)
