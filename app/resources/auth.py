from flask_restful import Resource
from flask_restful import reqparse
from app.utils import response
from app.utils import RespCode
from app.utils import generate_token
from app.utils import verify_token
from app.utils import open_invitation
from app.utils import resolve_token
from app.utils import check_permission
from app.models.user import UserModel


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        args = parser.parse_args()

        user: UserModel = UserModel.find(username=args['username'])[0]

        if user.check_password(args['password']):
            data = {'token': generate_token(**user.to_dict())}
            return response(RespCode.OK, 'login success', data)


class VerifyResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        args = parser.parse_args()

        return response(1, '验证成功', verify_token(args['token']))


class InvitationResource(Resource):
    def get(self):
        # 只用超级用户可以查看邀请码
        check_permission(resolve_token(), ['superuser'], ['superuser'])
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, location='args')
        args = parser.parse_args()

        invis = open_invitation()
        datas = []

        if (args['status'] == 'valid'):
            for invi in invis:
                if invi['valid']:
                    datas.append(invi)
        else:
            datas = invis

        return response(1, '获取 invitation 成功 ', {
            'invitations': datas,
        })
