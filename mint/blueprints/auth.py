from flask import Blueprint

from mint.utils import gen_invitation
from mint.utils import open_invitation
from mint.models import UserModel
from mint.exceptions import IncorrectInfo
from mint.utils.auth import PermCheck
from mint.utils.auth import resolve_token
from mint.utils.auth import generate_token
from mint.utils.auth import get_sts_credential
from mint.utils.parser import Parser
from mint.utils.reponse import response
from mint.utils.reponse import find_success

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/invitation/list")
def get_invitation_list():
    PermCheck.superuser()
    status = Parser.parse_args(status=str).get("status")

    invis = open_invitation()
    datas = []

    if status == "valid":
        for invi in invis:
            if invi["valid"]:
                datas.append(invi)
    else:
        datas = invis

    return find_success({"invitations": datas})


@auth_bp.post("/genInvitations")
def gen_invitation_list():
    PermCheck.superuser()
    gen_invitation()
    return response(0, "生成邀请码成功")


@auth_bp.post("/token")
def get_token():
    kw = Parser.parse_json(username=str, password=str)
    users, counts = UserModel.find(username=kw.get("username"))

    if not users[0].check_password(kw.get("password")):
        raise IncorrectInfo

    return response(0, "获取 TOKEN 成功", {"token": generate_token(**users[0].to_dict())})


@auth_bp.get("/sts")
def sts_server():
    PermCheck.common_above()
    username = resolve_token().get("username")
    kw = Parser.parse_args(bucket=str, region=str, action=str)

    credits = get_sts_credential(username, **kw)

    return response(0, "获取 STS 成功", credits)
