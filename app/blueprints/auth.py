from flask import Blueprint
from app.models import UserModel
from app.utils.reponse import find_success
from app.utils.reponse import response
from app.utils.parser import Parser
from app.utils.auth import PermCheck
from app.utils.auth import generate_token
from app.utils import open_invitation
from app.exceptions import IncorrectInfo


auth_bp = Blueprint('auth', __name__)


@auth_bp.get('/invitation/list')
def get_invitation_list():
    PermCheck.superuser()
    status = Parser.parse_args(status=str).get('status')

    invis = open_invitation()
    datas = []

    if (status == 'valid'):
        for invi in invis:
            if invi['valid']:
                datas.append(invi)
    else:
        datas = invis

    return find_success({'invitations': datas})


@auth_bp.post('/token')
def get_token():
    kw = Parser.parse_json(username=str, password=str)
    user: UserModel = UserModel.find(username=kw.get('username'))[0]

    if not user.check_password(kw.get('password')):
        raise IncorrectInfo

    return response(0, '获取 TOKEN 成功', {
        'token': generate_token(**user.to_dict())
    })
