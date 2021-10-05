from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from core.crypto import cipher


class EncryptedStr(str):
    @property
    def decrypted(self):
        return cipher.decrypt(str(self))

    @classmethod
    def encrypt(cls, value: str) -> 'EncryptedStr':
        return cls(cipher.encrypt(value))


class UserModel(BaseModel):
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    created_at: datetime = Field(default_factory=datetime.utcnow)

    zenmoney_token: Optional[EncryptedStr]
