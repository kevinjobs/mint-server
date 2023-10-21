import os
import time
import json
from datetime import datetime
from datetime import timedelta
from flask import request
import jwt
from shortuuid import uuid


SALT = '&(^d)daga234235gfd&*NDF9d8fa&kda(234daf))Ngd23@#%DSFGdf235'


class RespCode:
    OK = 0
    ERROR = 1
    DB_ERROR = 9001
    NOT_FOUND = 4004
    EXISTED = 5001
    NO_PERMISSION = 4000
    NOT_ALLOWED = 4007
    INVALID_INVITATION = 8001
    INVALID_TOKEN = 8002


class RespMsg:
    OK = 'request success'
    ERROR = 'unknown error'
    DB_ERROR = 'database error'
    NOT_FOUND = 'the resource doesnt exist'
    EXISTED = 'the resource existed'
    NO_PERMISSION = 'no permission to access'
    NOT_ALLOWED = 'not allowed'
    INVALID_INVITATION = '无效的邀请码'
    INVALID_TOKEN = 'TOKEN 无效或者已经过期'


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


def save_success():
    return response(RespCode.OK, 'save success')


def find_success(data):
    return response(RespCode.OK, 'find success', data)


def del_success():
    return response(RespCode.OK, 'delete success')


def update_success():
    return response(RespCode.OK, 'update success')


def generate_token(**kw):
    """generate a json web token

    Returns:
        str: json web token
    """
    payload = {**kw, 'exp': datetime.utcnow() + timedelta(days=3)}
    params = {
        'payload': payload,
        'key': SALT,
        'algorithm': 'HS256',
        'headers': {'typ': 'jwt', 'alg': 'HS256'}
    }
    return jwt.encode(**params)


def verify_token(token):
    """verify the json web token

    Args:
        token (str): json web token

    Returns:
        Any: a dict includes payload or any
    """
    from app.exceptions import InvalidToken
    if token is None:
        raise InvalidToken('没有提供 TOKEN')

    try:
        payload = jwt.decode(token, SALT, algorithms=['HS256'])
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        raise InvalidToken('TOKEN 已经过期')
    except jwt.DecodeError:
        raise InvalidToken('无法解析 TOKEN')
    except jwt.InvalidTokenError:
        raise InvalidToken('无效的 TOKEN')


def resolve_token():
    token = extract_token()
    payload = verify_token(token)
    return payload


def extract_token():
    """extract Bearer string from Authorization

    Returns:
        string: token
    """
    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Bearer '):
        return auth[7:]


def ensure_path(path: str):
    """ensure the path exists

    Args:
        path (str): pathlike
    """
    if not os.path.exists(path):
        os.makedirs(path)


def now_stamp():
    return int(round(time.time() * 1000))


def check_permission(user, roles, groups):
    from app.exceptions import NoPermission
    if user.get('role') in roles or user.get('group') in groups:
        return True
    else:
        role = user.get('role')
        group = user.get('group')
        s = '没有访问权限，用户角色[{}]，需要{}，用户组[{}]，需要{}'
        raise NoPermission(s.format(role, roles, group, groups))


INVITATION_FILE = 'invitations.json'


def check_invitation(c: str):
    from app.exceptions import InvalidInvitation
    codes = open_invitation()

    i = 0
    for invi in codes:
        if invi['code'] == c and invi['valid']:
            return True
        i += 1

    raise InvalidInvitation('邀请码无效或者已经被使用')


def invalidate_invitation(c: str, username=None):
    codes = open_invitation()

    i = 0
    for invi in codes:
        if invi['code'] == c:
            codes[i]['valid'] = False
            codes[i]['registerAt'] = now_stamp()
            codes[i]['registerBy'] = username if username else ''
            with open(INVITATION_FILE, 'w') as fp:
                json.dump(codes, fp, ensure_ascii=False, indent=2)
            return True
        i += 1


def gen_invitation(counts=10):
    codes = []
    datas = open_invitation()
    for _ in range(0, counts):
        codes.append({
            "createAt": now_stamp(),
            "code": uuid(),
            "valid": True,
        })

    with open(INVITATION_FILE, 'w') as fp:
        json.dump(codes + datas, fp, ensure_ascii=False, indent=2)


def open_invitation():
    try:
        with open(INVITATION_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
