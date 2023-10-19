from datetime import datetime
from datetime import timedelta
from flask import request
import jwt


salt = '&(^d)daga234235gfd&*NDF9d8fa&kda(234daf))Ngd23@#%DSFGdf235'


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


def generate_token(**kw):
    payload = {**kw, 'exp': datetime.utcnow() + timedelta(days=3)}
    params = {
        'payload': payload,
        'key': salt,
        'algorithm': 'HS256',
        'headers': {'typ': 'jwt', 'alg': 'HS256'}
    }
    return jwt.encode(**params)


def verify_token(token):
    try:
        payload = jwt.decode(token, salt, algorithms=['HS256'])
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        return 1
    except jwt.DecodeError:
        return 2
    except jwt.InvalidTokenError:
        return 3


def extract_token():
    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Bearer '):
        return auth[7:]
