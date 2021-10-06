from libs.crypto import AESCipher

from .config import settings

cipher = AESCipher(settings.SECRET_KEY)
