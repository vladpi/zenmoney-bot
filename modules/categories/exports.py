from typing import TYPE_CHECKING, List, Optional

from .internals import create_from_zenmoney_tag
from .service import category_service

if TYPE_CHECKING:
    from libs.zenmoney.schemas import Tag

    from .schemas import CategoryModel


async def create_category_from_zenmoney_tag(user_id: int, tag: 'Tag') -> 'CategoryModel':
    return await create_from_zenmoney_tag(user_id, tag)


async def get_categories_by_user(user_id: int) -> List['CategoryModel']:
    return await category_service.get_by_user(user_id)


async def get_outcome_categories_by_user(user_id: int) -> List['CategoryModel']:
    return await category_service.get_outcome_by_user(user_id)


async def get_user_category_by_title(user_id: int, title: str) -> Optional['CategoryModel']:
    return await category_service.get_by_title(user_id, title)


async def delete_category(id_: str) -> None:
    return await category_service.delete(id_)


async def update_category_transactions_count(
    id_: str,
    transactions_count: Optional[int] = None,
) -> None:
    return await category_service.update_transactions_count(id_, transactions_count)
