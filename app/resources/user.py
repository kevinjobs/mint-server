from flask import g
from flask_restful import Resource
from flask_restful import reqparse

from app.models.user import UserModel
from app.utils import response
from app.utils import RespCode
from app.utils import find_success
from app.utils import update_success
from app.utils import del_success
from app.utils import save_success
from app.utils import generate_token
from app.utils import verify_token
from app.utils import check_permission
from app.utils import check_invitation
from app.utils import invalidate_invitation


class UserResource(Resource):
    def get(self):
        check_permission(g.user, ['admin', 'superuser'], ['admin'])
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='args')
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('nickname', type=str, location='args')
        args = parser.parse_args()
        rets = UserModel.find(**args)
        return find_success({
            'amount': len(rets),
            'users': [ret.to_dict() for ret in rets]
        })

    def post(self):
        '''add a new user
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        parser.add_argument('nickname', type=str, location='json')
        parser.add_argument('location', type=str, location='json')
        parser.add_argument('birthday', type=str, location='json')
        parser.add_argument('gender', type=str, location='json')
        parser.add_argument('role', type=str, location='json')
        parser.add_argument('group', type=str, location='json')
        parser.add_argument('invitation', type=str, location='json')
        args = parser.parse_args()
        # 检查验证是否有效，无效将直接抛出错误
        check_invitation(args['invitation'])
        # 保存到数据库中
        user = UserModel(**args)
        user.save()
        # 没有发生错误的情况下，使邀请码无效
        invalidate_invitation(args['invitation'])
        # 返回信息
        return save_success()

    def put(self):
        '''update a user
        '''
        check_permission(g.user, ['admin', 'superuser'], ['admin'])
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        parser.add_argument('nickname', type=str, location='json')
        parser.add_argument('location', type=str, location='json')
        parser.add_argument('birthday', type=str, location='json')
        parser.add_argument('gender', type=str, location='json')
        parser.add_argument('role', type=str, location='json')
        parser.add_argument('group', type=str, location='json')
        args = parser.parse_args()
        UserModel.update(**args)
        return update_success()

    # todo: 只有管理员和超级用户有权删除用户
    def delete(self):
        check_permission(g.user, ['admin', 'superuser'], ['admin'])
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        args = parser.parse_args()
        UserModel.delete_by_uid(args['uid'])
        return del_success()


class UsersResource(Resource):
    def get(self):
        check_permission(g.user, ['admin', 'superuser'], ['admin'])
        rets = UserModel.find()
        return find_success({
            "amount": len(rets),
            "users": [ret.to_dict() for ret in rets]
        })


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        args = parser.parse_args()

        user: UserModel = UserModel.find(username=args['username'])

        if user.check_password(args['password']):
            data = {'token': generate_token(**user.to_dict())}
            return response(RespCode.OK, 'login success', data)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        args = parser.parse_args()
        v = verify_token(args['token'])
        code = RespCode.OK
        msg = 'verify success'
        if v == 1:
            msg = 'token expired'
            code = RespCode.ERROR
        if v == 2:
            msg = 'cannot decode token'
            code = RespCode.ERROR
        if v == 3:
            msg = 'invalid token'
            msg = RespCode.ERROR
        return response(code, msg, v)
