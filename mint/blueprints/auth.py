from flask import Blueprint
from mint.models import UserModel
from mint.utils.reponse import find_success
from mint.utils.reponse import response
from mint.utils.parser import Parser
from mint.utils.auth import PermCheck
from mint.utils.auth import generate_token
from mint.utils import open_invitation
from mint.exceptions import IncorrectInfo


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
    users, counts = UserModel.find(username=kw.get('username'))

    if not users[0].check_password(kw.get('password')):
        raise IncorrectInfo

    return response(0, '获取 TOKEN 成功', {
        'token': generate_token(**users[0].to_dict())
    })
