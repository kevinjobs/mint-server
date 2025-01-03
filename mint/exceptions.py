from mint.utils.reponse import response
from mint.constants import RespCode
from mint.constants import RespMsg
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


class InvalidInvitation(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.INVALID_INVITATION
        self.code = RespCode.INVALID_INVITATION


class InvalidToken(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.INVALID_TOKEN
        self.code = RespCode.INVALID_TOKEN


class IncorrectInfo(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.INCORRET_INFO
        self.code = RespCode.INCORRET_INFO


class ParamsMissing(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else RespMsg.PARAMS_MISSING
        self.code = RespCode.PARAMS_MISSING
