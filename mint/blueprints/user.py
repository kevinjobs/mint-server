from flask import Blueprint
from mint.models import UserModel
from mint.utils.reponse import find_success
from mint.utils.reponse import save_success
from mint.utils.reponse import update_success
from mint.utils.reponse import del_success
from mint.utils.parser import Parser
from mint.utils.auth import PermCheck
from mint.utils import check_invitation
from mint.utils import invalidate_invitation


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.get('')
def get_user():
    PermCheck.common_above()
    kw = Parser.parse_args(uid=str, nickname=str, username=str)
    rets, counts = UserModel.find(**kw)
    return find_success({
        'totals': counts,
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

    # 注册时需验证邀请码
    args['invitation'] = str

    args['motto'] = str
    args['avatar'] = str
    args['description'] = str

    kw = Parser.parse_json(**args)
    # 验证邀请码
    check_invitation(kw.get('invitation'))
    UserModel(**kw).save()
    # 使邀请码无效
    invalidate_invitation(kw.get('invitation'), kw.get('username'))
    del kw['password']
    return save_success({'user': kw})


@user_bp.put('')
def update_user():
    PermCheck.admin_above()
    args = {}
    args['username'] = str
    args['password'] = str
    args['nickname'] = str

    args['gender'] = str
    args['birthday'] = int
    args['location'] = str

    # 暂时只允许 superuser 调整用户等级
    if PermCheck.is_superuser():
        args['role'] = str
        args['group'] = str

    args['motto'] = str
    args['avatar'] = str
    args['description'] = str

    uid = Parser.parse_args(uid=str).get('uid')
    kw = Parser.parse_json(**args)
    UserModel.update(uid=uid, **kw)
    return update_success()


@user_bp.delete('')
def delete_user():
    PermCheck.admin_above()
    kw = Parser.parse_args(uid=str)
    UserModel.delete_by_uid(kw['uid'])
    return del_success()


@user_bp.get('/list')
def get_user_list():
    PermCheck.admin_above()
    kw = Parser.parse_args(offset=int, limit=int, username=str, nickname=str)
    rets, counts = UserModel.find(**kw)
    return find_success({
        'totals': counts,
        'amount': len(rets),
        'users': [ret.to_dict() for ret in rets]
    })
