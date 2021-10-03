from typing import TYPE_CHECKING, Optional, Union

from core import database
from libs.base_service import BaseDBService

from .schemas import UserModel
from .tables import users

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny


class UserService(BaseDBService):
    async def put(  # type: ignore[override]
        self,
        instance: UserModel,
        allow_update: bool = True,
        exclude_from_update: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
    ) -> UserModel:
        if exclude_from_update is None:
            exclude_from_update = {'id', 'created_at'}

        return await super().put(
            instance,
            allow_update=allow_update,
            exclude_from_update={'id', 'created_at'},
        )


user_service = UserService(
    db=database,
    model_class=UserModel,
    table=users,
    pk_field=users.c.id,
)
