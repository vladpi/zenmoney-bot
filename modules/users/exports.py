from typing import Optional

from .internals import init_zenmoney_data, update_default_outcome_account, update_zenmoney_last_sync
from .schemas import UserModel
from .service import user_service


async def create_or_update_user(
    id_: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> UserModel:
    user = await user_service.get(id_)

    if user is None:
        user = UserModel(
            id=id_,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user = await user_service.put(user)

    return user


async def get_user(id_: int) -> Optional[UserModel]:
    return await user_service.get(id_)


async def init_user_zenmoney_data(
    user: UserModel,
    token: str,
    last_sync: int,
    user_id: int,
) -> UserModel:
    return await init_zenmoney_data(
        user=user,
        token=token,
        last_sync=last_sync,
        user_id=user_id,
    )


async def update_user_zenmoney_last_sync(user: 'UserModel', last_sync: int) -> 'UserModel':
    return await update_zenmoney_last_sync(user, last_sync)


async def update_user_default_outcome_account(
    user: 'UserModel',
    default_outcome_account: Optional[str],
) -> 'UserModel':
    return await update_default_outcome_account(user, default_outcome_account)
