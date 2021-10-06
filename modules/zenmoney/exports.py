from . import internals


def get_auth_url(user_id: int) -> str:
    return internals.get_auth_url(user_id)
