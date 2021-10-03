from typing import Optional

from .schemas import UserModel
from .service import user_service


async def create_or_update_user(
    id_: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> UserModel:
    user = UserModel(
        id=id_,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    return await user_service.put(user)


async def get_user(id_: int) -> Optional[UserModel]:
    return await user_service.get(id_)
