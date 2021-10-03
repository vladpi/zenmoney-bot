from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
