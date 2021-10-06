from core import database
from libs.base_service import BaseDBService

from .schemas import CategoryModel
from .tables import categories


class CategoryService(BaseDBService):
    pass


category_service = CategoryService(
    db=database,
    model_class=CategoryModel,
    table=categories,
    pk_field=categories.c.id,
)
