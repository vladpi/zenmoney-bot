import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key: str):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw: str) -> str:
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode('utf-8')

    def decrypt(self, enc: bytes) -> str:
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size :])).decode('utf-8')

    def _pad(self, s):
        bs = AES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]
