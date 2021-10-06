from typing import TYPE_CHECKING

from .internals import create_from_zenmoney_tag

if TYPE_CHECKING:
    from libs.zenmoney.schemas import Tag

    from .schemas import CategoryModel


async def create_category_from_zenmoney_tag(user_id: int, tag: 'Tag') -> 'CategoryModel':
    return await create_from_zenmoney_tag(user_id, tag)
