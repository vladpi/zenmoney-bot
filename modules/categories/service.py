from typing import List, Optional

import sqlalchemy as sa

from core import database
from libs.base_service import BaseDBService

from .schemas import CategoryModel
from .tables import categories


class CategoryService(BaseDBService):
    async def get_by_user(self, user_id: int) -> List[CategoryModel]:
        records = await self.db.fetch_all(
            sa.select([categories]).where(categories.c.user_id == user_id)
        )

        return [CategoryModel.parse_obj(record) for record in records]

    async def get_outcome_by_user(self, user_id: int) -> List[CategoryModel]:
        records = await self.db.fetch_all(
            sa.select([categories]).where(
                categories.c.user_id == user_id,
                categories.c.is_outcome,
            )
        )

        return [CategoryModel.parse_obj(record) for record in records]

    async def get_by_title(self, user_id: int, title: str) -> Optional[CategoryModel]:
        record = await self.db.fetch_one(
            sa.select([categories]).where(
                categories.c.user_id == user_id,
                categories.c.title == title,
            )
        )

        if record is not None:
            return CategoryModel.parse_obj(record)

        return None


category_service = CategoryService(
    db=database,
    model_class=CategoryModel,
    table=categories,
    pk_field=categories.c.id,
)
