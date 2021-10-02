from enum import Enum


class AccountType(str, Enum):
    CASH = 'cash'  # наличные
    CCARD = 'ccard'  # банковская карта
    CHECKING = 'checking'  # банковский счет
    LOAN = 'loan'  # кредит
    DEPOSIT = 'deposit'  # депозит
    EMONEY = 'emoney'  # электронные деньги (?)
    DEBT = 'debt'  # долги


class EndDateOffsetInterval(str, Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


class PayoffInterval(str, Enum):
    MONTH = 'month'
    YEAR = 'year'


class ReminderInterval(str, Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


class ReminderMarkerState(str, Enum):
    PLANNED = 'planned'  # планируемая
    PROCESSED = 'processed'  # обработанная
    DELETED = 'deleted'  # удаленная
