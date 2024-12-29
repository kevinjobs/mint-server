from functools import wraps

from mint.utils.auth import PermCheck


def auth_required(allows=None):
    if allows is None:
        allows = ['common']

    @wraps(allows)
    def deco(func):
        @wraps(func)
        def inner(*arg, **kw):
            if 'common' in allows:
                PermCheck.common_above()

            if 'admin' in allows:
                PermCheck.admin_above()

            if 'superuser' in allows:
                PermCheck.admin_above()

            return func(*arg, **kw)

        return inner

    return deco
