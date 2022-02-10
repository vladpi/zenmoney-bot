from typing import TYPE_CHECKING, List, Optional

import sqlalchemy as sa

from core import database
from libs.base_service import BaseDBService

from .schemas import CategoryModel
from .tables import categories

if TYPE_CHECKING:
    from sqlalchemy.sql.selectable import Select


class CategoryService(BaseDBService):
    async def get_by_user(self, user_id: int) -> List[CategoryModel]:
        records = await self.db.fetch_all(
            self._sorted_query(sa.select([categories]).where(categories.c.user_id == user_id))
        )

        return [CategoryModel.parse_obj(record) for record in records]

    async def get_outcome_by_user(self, user_id: int) -> List[CategoryModel]:
        records = await self.db.fetch_all(
            self._sorted_query(
                sa.select([categories]).where(
                    categories.c.user_id == user_id,
                    categories.c.is_outcome,
                )
            )
        )

        return [CategoryModel.parse_obj(record) for record in records]

    async def get_by_title(self, user_id: int, title: str) -> Optional[CategoryModel]:
        record = await self.db.fetch_one(
            self._sorted_query(
                sa.select([categories]).where(
                    categories.c.user_id == user_id,
                    categories.c.title == title,
                )
            )
        )

        if record is not None:
            return CategoryModel.parse_obj(record)

        return None

    async def update_transactions_count(
        self,
        id_: str,
        value: Optional[int] = None,
    ) -> None:
        await self.db.execute(
            sa.update(self.table)
            .where(self.table.c.id == id_)
            .values(
                transactions_count=self.table.c.transactions_count + 1 if value is None else value
            )
        )

    def _sorted_query(self, query: 'Select') -> 'Select':
        return query.order_by(sa.desc(self.table.c.transactions_count))


category_service = CategoryService(
    db=database,
    model_class=CategoryModel,
    table=categories,
    pk_field=categories.c.id,
)
