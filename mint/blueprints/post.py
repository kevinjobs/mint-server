from flask import Blueprint

from mint.models import PostModel
from mint.decorators import auth_required
from mint.utils.parser import Parser
from mint.utils.reponse import del_success
from mint.utils.reponse import find_success
from mint.utils.reponse import save_success
from mint.utils.reponse import update_success

post_bp = Blueprint("post", __name__)


ARGS = {
    "createAt": str,
    "updateAt": str,
    "publishAt": str,
    "type": str,
    "title": str,
    "author": str,
    "content": str,
    "excerpt": str,
    "url": str,
    "status": str,
    "tags": str,
    "category": str,
    "format": str,
    "exif": str,
    "description": str,
}


@post_bp.get("/p")
def get_post():
    kw = Parser.parse_args(uid=str, title=str)
    rets, counts = PostModel.find(**kw)
    return find_success({"post": rets[0].to_dict()})


@post_bp.post("/p")
@auth_required(["common"])
def add_post():
    kw = Parser.parse_json(**ARGS)
    PostModel(**kw).save()
    return save_success()


@post_bp.put("/p")
@auth_required(["common"])
def update_post():
    uid = Parser.parse_args(uid=str).get("uid")
    kw = Parser.parse_json(**ARGS)
    PostModel.update(uid=uid, **kw)
    return update_success()


@post_bp.delete("/p")
@auth_required(["common"])
def delete_post():
    uid = Parser.parse_args(uid=str).get("uid")
    PostModel.delete_by_uid(uid)
    return del_success()


@post_bp.get("/post/list")
def get_post_list():
    args = {"status": str, "author": str, "category": str, "format": str, "type": str, "offset": int, "limit": int}

    kw = Parser.parse_args(**args)
    rets, counts = PostModel.find(**kw)
    return find_success(
        {
            "totals": counts,
            "amount": len(rets),
            "offset": kw.get("offset") or 0,
            "limit": kw.get("limit") or 10,
            "posts": [ret.to_dict() for ret in rets],
        }
    )
