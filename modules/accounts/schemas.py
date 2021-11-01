from pydantic import BaseModel


class AccountModel(BaseModel):
    id: str
    user_id: int
    instrument_id: int

    title: str
