from functools import wraps


def auth_required(user, allow):
    @wraps(user, allow)
    def deco(func):
        @wraps(func)
        def inner(*arg, **kw):
            return func(*arg, **kw)

        return inner

    return deco
