from typing import List
from flask import Blueprint
from flask import request
from app.models import UserModel
from app.utils import find_success
from app.utils import save_success


user_bp = Blueprint('user', __name__, url_prefix='/test')


def resolve_args(**kw):
    params = {}
    for k, v in kw.items():
        value = request.args.get(k)
        if value:
            params[k] = v(value)
    return params


def parse_json(**kw):
    params = {}
    for k, v in kw.items():
        value = request.json.get(k)
        if value:
            params[k] = v(value)
    return params


@user_bp.get('')
def get_user():
    args = resolve_args(uid=str, nickname=str, filename=str)
    rets = UserModel.find(**args)
    return find_success({
        'amount': len(rets),
        'users': [ret.to_dict() for ret in rets]
    })


@user_bp.post('')
def register():
    args = {}
    args['username'] = str
    args['password'] = str
    args['nickname'] = str
    args['location'] = str
    args['birthday'] = str
    args['gender'] = str
    args['invitation'] = str

    json = parse_json(**args)
    UserModel(**json).save()
    return save_success()
