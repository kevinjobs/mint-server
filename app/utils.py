class RespCode:
    OK = 1
    ERROR = 0
    DB_ERROR = 9001
    NOT_FOUND = 4004
    EXISTED = 5001


class RespMsg:
    OK = 'request success'
    ERROR = 'unknown error'
    DB_ERROR = 'database error'
    NOT_FOUND = 'the resource doesnt exist'
    EXISTED = 'the resource existed'


def response(code: int, msg: str, data=None):
    r = {
        'code': code,
        'msg': msg,
    }
    if data:
        r['data'] = data
    return r
