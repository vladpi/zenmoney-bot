from typing import TYPE_CHECKING, Optional

from .schemas import EncryptedStr
from .service import user_service

if TYPE_CHECKING:
    from .schemas import UserModel


async def init_zenmoney_data(
    user: 'UserModel',
    token: str,
    last_sync: int,
    user_id: int,
) -> 'UserModel':
    user.zenmoney_user_id = user_id
    user.zenmoney_token = EncryptedStr.encrypt(token)
    user.zenmoney_last_sync = last_sync
    return await user_service.put(user)


async def update_zenmoney_last_sync(user: 'UserModel', last_sync: int) -> 'UserModel':
    user.zenmoney_last_sync = last_sync
    return await user_service.put(user)


async def update_default_outcome_account(
    user: 'UserModel',
    default_outcome_account: Optional[str],
) -> 'UserModel':
    user.default_outcome_account_id = default_outcome_account
    return await user_service.put(user)
