from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

if TYPE_CHECKING:
    from databases import Database
    from pydantic import BaseModel
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny
    from sqlalchemy import Column, Table

    BaseModelType = TypeVar('BaseModelType', bound=BaseModel)


class BaseDBService:
    def __init__(
        self,
        db: 'Database',
        model_class: Type['BaseModelType'],
        table: 'Table',
        pk_field: 'Column',
    ):
        self.db = db
        self.model_class = model_class
        self.table = table
        self.pk_field = pk_field

    async def put(
        self,
        instance: 'BaseModelType',
        allow_update: bool = True,
        exclude_from_update: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
    ) -> 'BaseModelType':
        query = insert(self.table).values(instance.dict()).returning(self.table)

        if allow_update:
            query = query.on_conflict_do_update(
                index_elements=[self.pk_field],
                set_=instance.dict(exclude=exclude_from_update),  # type: ignore
            )

        record = await self.db.fetch_one(query)

        return self.model_class.parse_obj(record)

    async def get(self, id_: Any) -> Optional['BaseModelType']:
        query = sa.select([self.table]).where(self.pk_field == id_)

        record = await self.db.fetch_one(query)

        if record is not None:
            return self.model_class.parse_obj(record)

        return None
