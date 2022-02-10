from pydantic import BaseModel


class CategoryModel(BaseModel):
    id: str
    user_id: int

    title: str
    is_income: bool
    is_outcome: bool

    transactions_count: int = 0
