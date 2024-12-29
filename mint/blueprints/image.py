from flask import Blueprint

from mint.models import ImageModel
from mint.decorators import auth_required
from mint.utils.parser import Parser
from mint.utils.reponse import del_success
from mint.utils.reponse import find_success
from mint.utils.reponse import save_success
from mint.utils.reponse import update_success

image_bp = Blueprint("image", __name__)

ARGS = {
    "createAt": str,
    "updateAt": str,
    "title": str,
    "author": str,
    "description": str,
    "width": int,
    "height": int,
    "latitude": float,
    "longitude": float,
    "latitudeRef": str,
    "longitudeRef": str,
    "altitude": str,
    "altitudeRef": str,
    "aperture": str,
    "focalLength": str,
    "iso": int,
    "exposure": str,
    "lens": str,
    "model": str,
    "uri": str,
}


@image_bp.get("/image")
def get_image():

    kw = Parser.parse_args(uid=str)

    rets, counts = ImageModel.find(**kw)

    return find_success({"image": rets[0].to_dict()})


@image_bp.delete("/image")
@auth_required(["common"])
def delete_image():

    uid = Parser.parse_args(uid=str).get("uid")

    ImageModel.delete_by_uid(uid)
    return del_success()


@image_bp.put("/image")
@auth_required(["common"])
def update_post():

    uid = Parser.parse_args(uid=str).get("uid")

    kw = Parser.parse_json(**ARGS)

    ImageModel.update(uid=uid, **kw)
    return update_success()


@image_bp.get("/image-list")
def get_image_list():

    list_args = {"title": str, "author": str, "offset": int, "limit": int}

    kw = Parser.parse_args(**list_args)

    rets, counts = ImageModel.find(**kw)
    return find_success(
        {
            "totals": counts,
            "amount": len(rets),
            "offset": kw.get("offset") or 0,
            "limit": kw.get("limit") or 10,
            "images": [ret.to_dict() for ret in rets],
        }
    )


@image_bp.post("/image")
@auth_required(["common"])
def post_image():

    data = Parser.parse_json(**ARGS)

    image = ImageModel(**data)

    image.save()

    return save_success()
