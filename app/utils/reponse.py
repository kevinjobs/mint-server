from app.constants import RespCode


def save_success(data=None):
    return response(RespCode.OK, 'save success', data)


def find_success(data):
    return response(RespCode.OK, 'find success', data)


def del_success(data=None):
    return response(RespCode.OK, 'delete success', data)


def update_success(data=None):
    return response(RespCode.OK, 'update success', data)


def response(code: int, msg: str, data=None):
    """http response

    Args:
        code (int): self-defined code
        msg (str): http response message
        data (dict, optional): response data. Defaults to None.

    Returns:
        dict: response
    """
    r = {
        'code': code,
        'msg': msg,
    }
    if data:
        r['data'] = data
    return r
