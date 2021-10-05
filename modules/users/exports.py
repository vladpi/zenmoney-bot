from typing import Optional

from .internals import update_zenmoney_token
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


async def update_user_zenmoney_token(user: UserModel, token: str) -> UserModel:
    return await update_zenmoney_token(user, token)
