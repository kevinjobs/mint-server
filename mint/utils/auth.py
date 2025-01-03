import os
import jwt
import json
from datetime import datetime
from datetime import timedelta
from flask import request

from sts.sts import Sts
from sts.sts import Scope

from mint.constants import SecretCode
from mint.exceptions import InvalidToken
from mint.exceptions import NoPermission


def verify_token(token):
    """verify the json web token

    Args:
        token (str): json web token

    Returns:
        Any: a dict includes payload or any
    """
    if token is None:
        raise InvalidToken('没有提供 TOKEN')

    try:
        payload = jwt.decode(token, SecretCode.SALT, algorithms=['HS256'])
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        raise InvalidToken('TOKEN 已经过期')
    except jwt.DecodeError:
        raise InvalidToken('无法解析 TOKEN')
    except jwt.InvalidTokenError:
        raise InvalidToken('无效的 TOKEN')


def resolve_token():
    """获取 token 中的内容
    Return: 用于生成 token 的内容
    """
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


def generate_token(**kw):
    """generate a json web token

    Returns:
        str: json web token
    """
    payload = {**kw, 'exp': datetime.utcnow() + timedelta(days=3)}
    params = {
        'payload': payload,
        'key': SecretCode.SALT,
        'algorithm': 'HS256',
        'headers': {'typ': 'jwt', 'alg': 'HS256'}
    }
    return jwt.encode(**params)


class PermCheck:
    @staticmethod
    def superuser():
        return PermCheck.check_permission(
            resolve_token(),
            ['superuser'],
            ['superuser']
        )

    @staticmethod
    def admin_above():
        """用户级别是否为管理员以上

        Returns:
            bool: 检查通过返回 True 否则抛出错误
        """
        return PermCheck.check_permission(
            resolve_token(),
            ['admin', 'superuser'],
            ['admin']
        )

    @staticmethod
    def common_above():
        """用户级别是否为注册用户以上

        Returns:
            bool: 检查通过返回 True 否则抛出错误
        """
        return PermCheck.check_permission(
            resolve_token(),
            ['common', 'admin', 'superuser'],
            ['admin']
        )

    @staticmethod
    def check_permission(user, roles, groups):
        if user.get('role') in roles or user.get('group') in groups:
            return True
        else:
            role = user.get('role')
            group = user.get('group')
            s = '没有访问权限，用户角色[{}]，需要{}，用户组[{}]，需要{}'
            raise NoPermission(s.format(role, roles, group, groups))


def get_sts_credential(username: str, **options):
    action = options.get('action') or '*'
    bucket = options.get('bucket') or r'gallery-1252473272'
    region = options.get('region') or r'ap-nanjing'
    
    prefix = f'photos/{username}/*'

    scopes = list()
    scopes.append(Scope(action, bucket, region, prefix))

    config = {
        'sts_scheme': 'https',
        'sts_url': 'sts.tencentcloudapi.com',
        'duration_seconds': options.get('duration') or 1800,
        'secret_id': os.getenv('COS_SECRET_ID'),
        'secret_key': os.getenv('COS_SECRET_KEY'),
        'region': 'ap-nanjing',
        'policy': Sts.get_policy(scopes)
    }

    sts = Sts(config)
    resp = sts.get_credential()
    return resp
