from flask import Blueprint

from mint.models import ImageModel
from mint.utils.parser import Parser
from mint.utils.reponse import del_success, find_success, save_success, update_success

image_bp = Blueprint("image", __name__)


@image_bp.get("/image")
def get_image():
    kw = Parser.parse_args(uid=str)
    rets, counts = ImageModel.find(**kw)
    return find_success({"image": rets[0].to_dict()})


@image_bp.delete("/image")
def delete_image():
    PermCheck.admin_above()
    uid = Parser.parse_args(uid=str).get("uid")
    ImageModel.delete_by_uid(uid)
    return del_success()


@image_bp.put("/image")
def update_post():
    ARGS = {}
    ARGS["createAt"] = str
    ARGS["updateAt"] = str
    #
    ARGS["title"] = str
    ARGS["author"] = str
    ARGS["description"] = str
    #
    ARGS["width"] = int
    ARGS["height"] = int
    #
    ARGS["latitude"] = float
    ARGS["longitude"] = float
    ARGS["latitudeRef"] = str
    ARGS["longitudeRef"] = str
    ARGS["altitude"] = str
    ARGS["altitudeRef"] = str
    #
    ARGS["aperture"] = str
    ARGS["focalLength"] = str
    ARGS["iso"] = int
    ARGS["exposure"] = str
    ARGS["lens"] = str
    ARGS["model"] = str
    #
    ARGS["uri"] = str

    PermCheck.common_above()
    uid = Parser.parse_args(uid=str).get("uid")
    kw = Parser.parse_json(**ARGS)
    ImageModel.update(uid=uid, **kw)
    return update_success()


@image_bp.get("/image-list")
def get_image_list():
    args = {}
    args["title"] = str
    args["author"] = str

    args["offset"] = int
    args["limit"] = int

    kw = Parser.parse_args(**args)

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
def post_image():
    ARGS = {}
    ARGS["createAt"] = str
    ARGS["updateAt"] = str
    #
    ARGS["title"] = str
    ARGS["author"] = str
    ARGS["description"] = str
    #
    ARGS["width"] = int
    ARGS["height"] = int
    #
    ARGS["latitude"] = float
    ARGS["longitude"] = float
    ARGS["latitudeRef"] = str
    ARGS["longitudeRef"] = str
    ARGS["altitude"] = str
    ARGS["altitudeRef"] = str
    #
    ARGS["aperture"] = str
    ARGS["focalLength"] = str
    ARGS["iso"] = int
    ARGS["exposure"] = str
    ARGS["lens"] = str
    ARGS["model"] = str
    #
    ARGS["uri"] = str

    data = Parser.parse_json(**ARGS)
    image = ImageModel(**data)
    image.save()
    return save_success()
