from libs.zenmoney.client import ZenMoneyAPIClient

from .config import settings

zenmoney_client = ZenMoneyAPIClient(key=settings.ZENMONEY_KEY, secret=settings.ZENMONEY_SECRET)
