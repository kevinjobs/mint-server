from app.utils import response
from app.utils import RespCode
from app.utils import RespMsg
from werkzeug.exceptions import HTTPException


class RestfulError(HTTPException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code = self.name if isinstance(self.name, int) else RespCode.ERROR
        self.msg = \
            self.description \
            if isinstance(self.description, str) else RespMsg.ERROR

    def resp(self):
        return response(self.code, self.msg)


class DBError(RestfulError):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.DB_ERROR
        self.code = RespCode.DB_ERROR


class Existed(RestfulError):
    def __init__(self, *args):
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.EXISTED
        self.code = RespCode.EXISTED


class NotFound(RestfulError):
    def __init__(self, *args):
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.NOT_FOUND
        self.code = RespCode.NOT_FOUND


class NoPermission(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.NO_PERMISSION
        self.code = RespCode.NO_PERMISSION


class NotAllowed(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.NOT_ALLOWED
        self.code = RespCode.NOT_ALLOWED
