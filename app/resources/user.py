from flask import g
from flask_restful import Resource
from flask_restful import reqparse

from app.models.user import UserModel
from app.utils import response
from app.utils import RespCode
from app.utils import generate_token
from app.utils import verify_token


class UserResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='args')
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('nickname', type=str, location='args')
        args = parser.parse_args()

        if args.get('uid'):
            user: UserModel = UserModel.find_one_by_uid(args['uid'])
            return response(RespCode.OK, 'user found', user.to_dict())

        if args.get('username'):
            user: UserModel = UserModel.find_one_by_username(args['username'])
            return response(RespCode.OK, 'user found', user.to_dict())

        if args.get('nickname'):
            users: list[UserModel] = None
            users = UserModel.find_many_by_nickname(args['nickname'])
            data = [user.to_dict() for user in users]
            return response(RespCode.OK, 'users found', data)

        return response(RespCode.ERROR, 'send username, uid, or nickname')

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
        args = parser.parse_args()
        user = UserModel(**args)
        user.save()
        return response(RespCode.OK, 'add user success')

    def put(self):
        '''update a user
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
        args = parser.parse_args()
        user = UserModel.update_by_username(**args)
        return response(RespCode.OK, 'update user success', user.to_dict())

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        args = parser.parse_args()

        # 只有管理员和超级用户有权删除用户
        if not (g.user['role'] == 'admin' or g.user['role'] == 'superuser'):
            return response(RespCode.ERROR, 'permission denied.')

        UserModel.delete_by_uid(args['uid'])
        return response(RespCode.OK, 'delete user success')


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        args = parser.parse_args()

        user = UserModel.find_one_by_username(args['username'])

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
