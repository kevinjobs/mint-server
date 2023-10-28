from flask import Blueprint
from app.models import PostModel
from app.utils.reponse import find_success
from app.utils.reponse import save_success
from app.utils.reponse import update_success
from app.utils.reponse import del_success
from app.utils.parser import Parser
from app.utils.auth import PermCheck


post_bp = Blueprint('post', __name__)


ARGS = {}
ARGS['createAt'] = str
ARGS['updateAt'] = str
ARGS['publishAt'] = str
ARGS['type'] = str
ARGS['title'] = str
ARGS['author'] = str
ARGS['content'] = str
ARGS['excerpt'] = str
ARGS['url'] = str
ARGS['status'] = str
ARGS['tags'] = str
ARGS['category'] = str
ARGS['format'] = str
ARGS['exif'] = str
ARGS['description'] = str


@post_bp.get('/p')
def get_post():
    kw = Parser.parse_args(uid=str, title=str)
    rets, counts = PostModel.find(**kw)
    return find_success({'post': rets[0].to_dict()})


@post_bp.post('/p')
def add_post():
    PermCheck.common_above()
    kw = Parser.parse_json(**ARGS)
    PostModel(**kw).save()
    return save_success()


@post_bp.put('/p')
def update_post():
    PermCheck.common_above()
    uid = Parser.parse_args(uid=str).get('uid')
    kw = Parser.parse_json(**ARGS)
    PostModel.update(uid=uid, **kw)
    return update_success()


@post_bp.delete('/p')
def delete_post():
    PermCheck.admin_above()
    uid = Parser.parse_args(uid=str).get('uid')
    PostModel.delete_by_uid(uid)
    return del_success()


@post_bp.get('/post/list')
def get_post_list():
    args = {}
    args['status'] = str
    args['author'] = str
    args['category'] = str
    args['format'] = str
    args['type'] = str
    args['offset'] = int
    args['limit'] = int
    kw = Parser.parse_args(**args)
    rets, counts = PostModel.find(**kw)
    return find_success({
        'totals': counts,
        'amount': len(rets),
        'offset': kw.get('offset') or 0,
        'limit': kw.get('limit') or 10,
        'posts': [ret.to_dict() for ret in rets]
    })
