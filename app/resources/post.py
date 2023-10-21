from flask_restful import Resource
from flask_restful import reqparse

from app.models.post import PostModel
from app.utils import save_success
from app.utils import find_success
from app.utils import del_success
from app.utils import update_success
from app.utils import resolve_token
from app.utils import check_permission


class PostResource(Resource):
    def post(self):
        # 注册用户以上可以 post
        check_permission(
            resolve_token(),
            ['common', 'admin', 'superuser'],
            ['admin']
        )

        parser = reqparse.RequestParser()
        parser.add_argument('createAt', type=int, location='json')
        parser.add_argument('publishAt', type=int, location='json')
        parser.add_argument('updateAt', type=int, location='json')
        parser.add_argument('type', type=str, location='json')
        parser.add_argument('title', type=str, location='json')
        parser.add_argument('author', type=str, location='json')
        parser.add_argument('content', type=str, location='json')
        parser.add_argument('excerpt', type=str, location='json')
        parser.add_argument('cover', type=str, location='json')
        parser.add_argument('status', type=str, location='json')
        parser.add_argument('tags', type=str, location='json')
        parser.add_argument('category', type=str, location='json')
        parser.add_argument('format', type=str, location='json')
        parser.add_argument('url', type=str, location='json')
        parser.add_argument('exif', type=str, location='json')
        parser.add_argument('description', type=str, location='json')
        args = parser.parse_args()
        post = PostModel(**args)
        post.save()
        return save_success()

    def get(self):
        # 普通用户即可获取 post
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('title', type=str, location='args')
        args = parser.parse_args()
        posts: PostModel = PostModel.find(**args)
        return find_success({'post': posts[0].to_dict()})

    def delete(self):
        # 管理员以上可以删除 post
        check_permission(
            resolve_token(),
            ['admin', 'superuser'],
            ['admin']
        )
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        args = parser.parse_args()
        PostModel.delete_by_uid(args['uid'])
        return del_success()

    def put(self):
        # 普通用户以上可以更新 post
        check_permission(
            resolve_token(),
            ['common', 'admin', 'superuser'],
            ['admin']
        )
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('createAt', type=int, location='json')
        parser.add_argument('publishAt', type=int, location='json')
        parser.add_argument('updateAt', type=int, location='json')
        parser.add_argument('type', type=str, location='json')
        parser.add_argument('title', type=str, location='json')
        parser.add_argument('author', type=str, location='json')
        parser.add_argument('content', type=str, location='json')
        parser.add_argument('excerpt', type=str, location='json')
        parser.add_argument('cover', type=str, location='json')
        parser.add_argument('status', type=str, location='json')
        parser.add_argument('tags', type=str, location='json')
        parser.add_argument('category', type=str, location='json')
        parser.add_argument('format', type=str, location='json')
        parser.add_argument('url', type=str, location='json')
        parser.add_argument('exif', type=str, location='json')
        parser.add_argument('description', type=str, location='json')
        args = parser.parse_args()
        PostModel.update(**args)
        return update_success()


class PostsResource(Resource):
    def get(self):
        # 普通用户即可获取所有文章
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, location='args')
        parser.add_argument('author', type=str, location='args')
        parser.add_argument('category', type=str, location='args')
        parser.add_argument('format', type=str, location='args')
        parser.add_argument('offset', type=int, location='args')
        parser.add_argument('limit', type=int, location='args')
        args = parser.parse_args()
        rets = PostModel.find(**args)
        return find_success({
            'amount': len(rets),
            'offset': args.get('offset') or 0,
            'limit': args.get('limit') or 10,
            'posts': [ret.to_dict() for ret in rets],
        })
