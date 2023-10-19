from typing import List
from functools import wraps


def auth_required(roles: List[str], groups: List[str]):
    @wraps(roles, groups)
    def deco(func):
        @wraps(func)
        def inner(*arg, **kw):
            return func(*arg, **kw)

        return inner

    return deco
