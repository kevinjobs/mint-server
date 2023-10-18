from flask_restful import Resource
from flask_restful import reqparse
from app.db import db
from app.models.user import UserModel
from app.utils import response
from app.utils import RespCode


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, location='args')
parser.add_argument('password', type=str, location='args')


class UserResource(Resource):
    def get(self):
        args = parser.parse_args()
        user = UserModel.find_by_username(args['username'])
        if user:
            return response(RespCode.OK, 'find user')

    def post(self):
        args = parser.parse_args()
        user = UserModel(
            username=args.get('username'),
            password=args.get('password')
        )
        user.save()
        return response(RespCode.OK, 'add user success')
    

class LoginResource(Resource):
    def post(self):
        args = parser.parse_args()
        user = UserModel(username=args['username'], password=args['password'])

        if not UserModel.find_by_username(args['username']):
            return response(RespCode.NOT_FOUND, 'not this user')

        if user.check_password(args['password']):
            return response(RespCode.OK, 'login success')
