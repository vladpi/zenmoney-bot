from typing import TYPE_CHECKING

from .schemas import CategoryModel
from .service import category_service

if TYPE_CHECKING:
    from libs.zenmoney.schemas import Tag


async def create_from_zenmoney_tag(user_id: int, tag: 'Tag') -> CategoryModel:
    category = CategoryModel(
        id=tag.id,
        user_id=user_id,
        title=tag.title,
        is_income=tag.show_income,
        is_outcome=tag.show_outcome,
    )
    return await category_service.put(category, exclude_from_update={'transactions_count'})
