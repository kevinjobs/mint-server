from flask_restful import Resource
from flask_restful import reqparse

from app.models.user import UserModel
from app.utils import find_success
from app.utils import update_success
from app.utils import del_success
from app.utils import save_success
from app.utils import resolve_token
from app.utils import check_permission
from app.utils import check_invitation
from app.utils import invalidate_invitation


class UserResource(Resource):
    def get(self):
        # 注册用户以上才可以查看用户信息
        check_permission(
            resolve_token(),
            ['common', 'admin', 'superuser'],
            ['admin']
        )

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
        # 无需登录即可注册用户
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        parser.add_argument('nickname', type=str, location='json')
        parser.add_argument('location', type=str, location='json')
        parser.add_argument('birthday', type=str, location='json')
        parser.add_argument('gender', type=str, location='json')
        # 注册时为默认的用户角色和等级，无法自定义
        # parser.add_argument('role', type=str, location='json')
        # parser.add_argument('group', type=str, location='json')
        parser.add_argument('invitation', type=str, location='json')
        args = parser.parse_args()
        # 检查验证是否有效，无效将直接抛出错误
        check_invitation(args['invitation'])
        # 保存到数据库中
        user = UserModel(**args)
        user.save()
        # 没有发生错误的情况下，使邀请码无效
        invalidate_invitation(args['invitation'], args['username'])
        # 返回信息
        return save_success()

    def put(self):
        '''update a user
        '''
        # 只有 admin 和 superuser 可以更新用户信息
        check_permission(resolve_token(), ['admin', 'superuser'], ['admin'])

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

    def delete(self):
        # 只有 admin 和 superuser 可以删除用户
        check_permission(resolve_token(), ['admin', 'superuser'], ['admin'])

        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        args = parser.parse_args()
        UserModel.delete_by_uid(args['uid'])
        return del_success()


class UsersResource(Resource):
    def get(self):
        # 只有 admin 和 superuser 可以查看所有用户
        check_permission(resolve_token(), ['admin', 'superuser'], ['admin'])

        rets = UserModel.find()
        return find_success({
            "amount": len(rets),
            "users": [ret.to_dict() for ret in rets]
        })
