from app.utils import response
from app.utils import RespCode
from app.utils import RespMsg


class RestfulError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code = RespCode.ERROR
        self.msg = RespMsg.ERROR

    @property
    def response(self):
        return response(self.code, self.msg)


class DBError(RestfulError):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.DB_ERROR
        self.code = RespCode.DB_ERROR


class Existed(RestfulError):
    def __init__(self, *args):
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.DB_ERROR
        self.code = RespCode.EXISTED


class NotFound(RestfulError):
    def __init__(self, *args):
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.DB_ERROR
        self.code = RespCode.NOT_FOUND


class NoPermission(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.NO_PERMISSION
        self.code = RespCode.NO_PERMISSION
