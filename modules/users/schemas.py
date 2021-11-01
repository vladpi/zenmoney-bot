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

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        return cls(v)

    def __repr__(self):
        return f'EncryptedStr({super().__repr__()})'


class UserModel(BaseModel):
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    created_at: datetime = Field(default_factory=datetime.utcnow)

    zenmoney_user_id: Optional[int]
    zenmoney_token: Optional[EncryptedStr]
    zenmoney_last_sync: Optional[int]
