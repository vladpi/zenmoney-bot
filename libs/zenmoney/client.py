from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from urllib.parse import urlencode

from httpx import AsyncClient, Auth

from .schemas import DiffRequest, DiffResponse, GetTokenResposne

if TYPE_CHECKING:
    from .schemas import (
        Budget,
        Company,
        DeletionObject,
        Instrument,
        Merchant,
        Reminder,
        ReminderMarker,
        Tag,
        Transaction,
        User,
    )


class BearerAuth(Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        yield request


class ZenMoneyAPIClient:
    BASE_URL = 'https://api.zenmoney.ru'

    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret

    def get_auth_url(self, redirect_url: str) -> str:
        params = {
            'response_type': 'code',
            'client_id': self.key,
            'redirect_uri': redirect_url,
        }

        return f'{self.BASE_URL}/oauth2/authorize/?{urlencode(params)}'

    async def get_token(self, auth_code: str, redirect_url: str) -> GetTokenResposne:
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.key,
            'client_secret': self.secret,
            'code': auth_code,
            'redirect_uri': redirect_url,
        }

        async with AsyncClient() as client:
            response = await client.post(f'{self.BASE_URL}/oauth2/token/', data=data)

        return GetTokenResposne(**response.json())

    async def diff(
        self,
        user_token: str,
        server_timestamp: int = 0,  # last sync unix timestamp
        force_fetch: Optional[List[str]] = None,
        instrument: Optional[List['Instrument']] = None,
        company: Optional[List['Company']] = None,
        user: Optional[List['User']] = None,
        tag: Optional[List['Tag']] = None,
        merchant: Optional[List['Merchant']] = None,
        budget: Optional[List['Budget']] = None,
        reminder: Optional[List['Reminder']] = None,
        reminder_marker: Optional[List['ReminderMarker']] = None,
        transaction: Optional[List['Transaction']] = None,
        deletion: Optional[List['DeletionObject']] = None,
    ) -> DiffResponse:
        data = DiffRequest(
            current_client_timestamp=int(datetime.utcnow().timestamp()),
            server_timestamp=server_timestamp,
            force_fetch=force_fetch,
            instrument=instrument,
            company=company,
            user=user,
            tag=tag,
            merchant=merchant,
            budget=budget,
            reminder=reminder,
            reminder_marker=reminder_marker,
            transaction=transaction,
            deletion=deletion,
        )

        async with AsyncClient() as client:
            response = await client.post(
                f'{self.BASE_URL}/v8/diff/',
                content=data.json(),
                headers={'Content-Type': 'application/json'},
                auth=BearerAuth(user_token),
            )
        return DiffResponse(**response.json())
