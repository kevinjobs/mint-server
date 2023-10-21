from flask_restful import Resource
from flask_restful import reqparse

from app.models.post import PostModel
from app.utils import save_success
from app.utils import find_success
from app.utils import del_success
from app.utils import update_success


class PostResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, location='json')
        parser.add_argument('author', type=str, location='json')
        parser.add_argument('content', type=str, location='json')
        parser.add_argument('excerpt', type=str, location='json')
        parser.add_argument('cover', type=str, location='json')
        parser.add_argument('status', type=str, location='json')
        parser.add_argument('tags', type=str, location='json')
        parser.add_argument('category', type=str, location='json')
        parser.add_argument('format', type=str, location='json')
        args = parser.parse_args()
        post = PostModel(**args)
        post.save()
        return save_success()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('title', type=str, location='args')
        args = parser.parse_args()
        posts: PostModel = PostModel.find(**args)
        return find_success({'post': posts[0].to_dict()})

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        args = parser.parse_args()
        PostModel.delete_by_uid(args['uid'])
        return del_success()

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('title', type=str, location='json')
        parser.add_argument('author', type=str, location='json')
        parser.add_argument('content', type=str, location='json')
        parser.add_argument('excerpt', type=str, location='json')
        parser.add_argument('cover', type=str, location='json')
        parser.add_argument('status', type=str, location='json')
        parser.add_argument('tags', type=str, location='json')
        parser.add_argument('category', type=str, location='json')
        parser.add_argument('format', type=str, location='json')
        args = parser.parse_args()
        PostModel.update(**args)
        return update_success()


class PostsResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, location='args')
        parser.add_argument('author', type=str, location='args')
        parser.add_argument('category', type=str, location='args')
        parser.add_argument('format', type=str, location='args')
        args = parser.parse_args()
        rets = PostModel.find(**args)
        return find_success({
            'amount': len(rets),
            'posts': [ret.to_dict() for ret in rets],
        })
