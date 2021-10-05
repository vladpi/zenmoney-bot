from core import database
from libs.base_service import BaseDBService

from .schemas import AccountModel
from .tables import accounts


class AccountService(BaseDBService):
    pass


account_service = AccountService(
    db=database,
    model_class=AccountModel,
    table=accounts,
    pk_field=accounts.c.id,
)
