from werkzeug.exceptions import HTTPException

from mint.constants import Response
from mint.utils.reponse import response


class RestfulError(HTTPException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code = self.name if isinstance(self.name, int) else Response.ERROR[0]
        self.msg = self.description if isinstance(self.description, str) else Response.ERROR[1]

    def resp(self):
        return response(self.code, self.msg)


class DBError(RestfulError):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else Response.DB_ERROR[1]
        self.code = Response.DB_ERROR[0]


class ExistedError(RestfulError):
    def __init__(self, *args):
        super().__init__(*args)
        self.msg = args[0] if args else Response.EXISTED[1]
        self.code = Response.EXISTED[0]


class NotFoundError(RestfulError):
    def __init__(self, *args):
        super().__init__(*args)
        self.msg = args[0] if args else Response.NOT_FOUND[1]
        self.code = Response.NOT_FOUND[0]


class NoPermissionError(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else Response.NO_PERMISSION[1]
        self.code = Response.NO_PERMISSION[0]


class NotAllowedError(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else Response.NOT_ALLOWED[1]
        self.code = Response.NOT_ALLOWED[0]


class InvalidInvitationError(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else Response.INVALID_INVITATION[1]
        self.code = Response.INVALID_INVITATION[0]


class InvalidTokenError(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else Response.INVALID_TOKEN[1]
        self.code = Response.INVALID_TOKEN[0]


class InvalidUserInfoError(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else Response.INVALID_USER_INFO[1]
        self.code = Response.INVALID_USER_INFO[0]


class ParamsMissingError(RestfulError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0] if args else Response.PARAMS_MISSING[1]
        self.code = Response.PARAMS_MISSING[0]
