from typing import TYPE_CHECKING, List, Optional

import sqlalchemy as sa

from core import database
from libs.base_service import BaseDBService

from .schemas import AccountModel
from .tables import accounts

if TYPE_CHECKING:
    from sqlalchemy.sql.selectable import Select


class AccountService(BaseDBService):
    async def get_by_user(self, user_id: int) -> List[AccountModel]:
        records = await self.db.fetch_all(
            self._sorted_query(sa.select([accounts]).where(accounts.c.user_id == user_id))
        )

        return [AccountModel.parse_obj(record) for record in records]

    async def get_by_title(self, user_id: int, title: str) -> Optional[AccountModel]:
        record = await self.db.fetch_one(
            self._sorted_query(
                sa.select([accounts]).where(
                    accounts.c.user_id == user_id,
                    accounts.c.title == title,
                )
            )
        )

        if record is not None:
            return AccountModel.parse_obj(record)

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


account_service = AccountService(
    db=database,
    model_class=AccountModel,
    table=accounts,
    pk_field=accounts.c.id,
)
