from mint.constants import Response


def save_success(data=None):
    return response(Response.OK[0], "save success", data)


def find_success(data):
    return response(Response.OK[0], "find success", data)


def del_success(data=None):
    return response(Response.OK[0], "delete success", data)


def update_success(data=None):
    return response(Response.OK[0], "update success", data)


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
        "code": code,
        "msg": msg,
    }
    if data:
        r["data"] = data
    return r
