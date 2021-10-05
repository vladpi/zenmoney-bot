from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, Field, validator

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny

from .consts import (
    AccountType,
    EndDateOffsetInterval,
    PayoffInterval,
    ReminderInterval,
    ReminderMarkerState,
)

"""
Docs: https://github.com/zenmoney/ZenPlugins/wiki/ZenMoney-API#Сущности-
"""


class ZenMoneyBaseModel(BaseModel):
    def dict(self, *args, **kwargs) -> 'DictStrAny':
        if 'exclude_none' not in kwargs:
            kwargs['exclude_none'] = True
        if 'by_alias' not in kwargs:
            kwargs['by_alias'] = True
        return super().dict(*args, **kwargs)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: int(v.timestamp()),
        }


class Instrument(ZenMoneyBaseModel):
    """Валюта"""

    id: int
    changed: datetime  # unix timestamp
    title: str
    short_title: str = Field(..., alias='shortTitle')
    symbol: str
    rate: float


class Company(ZenMoneyBaseModel):
    """Банк либо другая платежная организация, в которой могут существовать счета"""

    id: int
    changed: datetime  # unix timestamp
    title: str
    full_title: Optional[str] = Field(None, alias='fullTitle')
    www: Optional[str] = None
    country: Optional[str] = None


class User(ZenMoneyBaseModel):
    id: int
    changed: datetime  # unix timestamp
    login: Optional[str] = None
    currency: int
    parent: Optional[int] = None


class Account(ZenMoneyBaseModel):
    """Cчёт пользователя"""

    id: str  # uuid
    changed: datetime  # unix timestamp
    user: int
    role: Optional[int] = None
    instrument: Optional[int] = None
    company: Optional[int] = None
    type: AccountType
    title: str
    sync_id: Optional[List[str]] = Field(None, alias='syncID')

    balance: Optional[float] = None
    start_balance: float = Field(None, alias='startBalance')
    credit_limit: float = Field(None, alias='creditLimit')

    in_balance: bool = Field(..., alias='inBalance')
    savings: Optional[bool] = Field(None)
    enable_correction: bool = Field(..., alias='enableCorrection')
    enable_sms: bool = Field(..., alias='enableSMS')
    archive: bool

    capitalization: Optional[bool] = None
    percent: Optional[float] = None
    start_date: Optional[date] = Field(None, alias='startDate')
    end_date_offset: Optional[int] = Field(None, alias='endDateOffset')
    end_date_offset_interval: Optional[EndDateOffsetInterval] = Field(
        None, alias='endDateOffsetInterval'
    )
    payoff_step: Optional[int] = Field(None, alias='payoffStep')
    payoff_interval: Optional[PayoffInterval] = Field(None, alias='payoffInterval')


class Tag(ZenMoneyBaseModel):
    """Категория"""

    id: str  # uuid
    changed: datetime  # unix timestamp
    user: int

    title: str
    parent: Optional[str] = None
    icon: Optional[str] = None  # id
    picture: Optional[str] = None  # url
    color: Optional[int] = None

    show_income: bool = Field(..., alias='showIncome')
    show_outcome: bool = Field(..., alias='showOutcome')
    budget_income: bool = Field(..., alias='showOutcome')
    budget_outcome: bool = Field(..., alias='budgetOutcome')
    required: bool

    @validator('required', pre=True)
    def set_default_required(cls, value):
        if value in ('none', 'null', None):
            return True
        return value


class Merchant(ZenMoneyBaseModel):
    """Контрагент операции"""

    id: str  # uuid
    changed: datetime  # unix timestamp
    user: int
    title: str


class ReminderBaseModel(ZenMoneyBaseModel):
    id: str  # uuid
    changed: datetime  # unix timestamp
    user: int

    income_instrument: int = Field(..., alias='incomeInstrument')
    income_account: str = Field(..., alias='incomeAccount')
    income: float
    outcome_instrument: int = Field(..., alias='outcomeInstrument')
    outcome_account: str = Field(..., alias='outcomeAccount')
    outcome: float

    tag: Optional[List[str]] = None
    merchant: Optional[str] = None
    payee: Optional[str] = None
    comment: Optional[str] = None

    notify: bool


class Reminder(ReminderBaseModel):
    """Объект описывающий принцип создания планируемых операций"""

    interval: Optional[ReminderInterval] = None
    step: Optional[int] = None
    points: Optional[List[int]] = None
    start_date: date = Field(..., alias='startDate')
    end_date: Optional[date] = Field(None, alias='endDate')


class ReminderMarker(ReminderBaseModel):
    """Планируемая операция"""

    at_date: date = Field(..., alias='date')

    reminder: str
    state: ReminderMarkerState


class Transaction(ZenMoneyBaseModel):
    """Денежная операция"""

    id: str  # uuid
    changed: datetime  # unix timestamp
    created: datetime  # unix timestamp
    user: int
    deleted: bool
    hold: Optional[bool] = None

    income_instrument: int = Field(..., alias='incomeInstrument')
    income_account: str = Field(..., alias='incomeAccount')
    income: float
    outcome_instrument: int = Field(..., alias='outcomeInstrument')
    outcome_account: str = Field(..., alias='outcomeAccount')
    outcome: float

    tag: Optional[List[str]] = None
    merchant: Optional[str] = None
    payee: Optional[str] = None
    comment: Optional[str] = None

    at_date: date = Field(..., alias='date')

    mcc: Optional[int] = None

    reminder_marker: Optional[str] = None

    op_income: Optional[float] = Field(None, alias='opIncome')
    op_income_instrument: Optional[int] = Field(None, alias='opIncomeInstrument')
    op_outcome: Optional[float] = Field(None, alias='opOutcome')
    op_outcome_instrument: Optional[int] = Field(None, alias='opOutcomeInstrument')

    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Budget(ZenMoneyBaseModel):
    changed: datetime  # unix timestamp
    user: int

    tag: Optional[str] = None
    at_date: date

    income: float
    income_lock: bool = Field(..., alias='incomeLock')
    outcome: float
    outcome_lock: bool = Field(..., alias='outcomeLock')


class DeletionObject(ZenMoneyBaseModel):
    id: str
    object: str
    stamp: int
    user: int


class DiffResponse(ZenMoneyBaseModel):
    server_timestamp: int = Field(..., alias='serverTimestamp')  # unix timestamp

    force_fetch: Optional[List[str]] = None

    instrument: Optional[List[Instrument]] = None
    company: Optional[List[Company]] = None
    user: Optional[List[User]] = None
    account: Optional[List[Account]] = None
    tag: Optional[List[Tag]] = None
    merchant: Optional[List[Merchant]] = None
    budget: Optional[List[Budget]] = None
    reminder: Optional[List[Reminder]] = None
    reminder_marker: Optional[List[ReminderMarker]] = Field(None, alias='reminderMarker')
    transaction: Optional[List[Transaction]] = None

    deletion: Optional[List[DeletionObject]] = None


class DiffRequest(DiffResponse):
    current_client_timestamp: int = Field(..., alias='currentClientTimestamp')  # unix timestamp


class GetTokenResposne(BaseModel):
    access_token: Optional[str]
    token_type: Optional[str]
    expires_in: Optional[int]
    refresh_token: Optional[str]
    error: Optional[str]
