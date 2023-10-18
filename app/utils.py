class RespCode:
    OK = 1
    NOT_FOUND = 4004


def response(code: int, msg: str, data=None):
    r = {
        'code': code,
        'msg': msg,
    }
    if data:
        r['data'] = data
    return r
