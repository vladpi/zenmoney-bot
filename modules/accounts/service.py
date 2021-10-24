from typing import List, Optional

import sqlalchemy as sa

from core import database
from libs.base_service import BaseDBService

from .schemas import AccountModel
from .tables import accounts


class AccountService(BaseDBService):
    async def get_by_user(self, user_id: int) -> List[AccountModel]:
        records = await self.db.fetch_all(
            sa.select([accounts]).where(accounts.c.user_id == user_id)
        )

        return [AccountModel.parse_obj(record) for record in records]

    async def get_by_title(self, user_id: int, title: str) -> Optional[AccountModel]:
        record = await self.db.fetch_one(
            sa.select([accounts]).where(
                accounts.c.user_id == user_id,
                accounts.c.title == title,
            )
        )

        if record is not None:
            return AccountModel.parse_obj(record)

        return None


account_service = AccountService(
    db=database,
    model_class=AccountModel,
    table=accounts,
    pk_field=accounts.c.id,
)
