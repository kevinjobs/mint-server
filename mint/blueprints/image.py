from flask import Blueprint

from mint.models import ImageModel
from mint.utils.parser import Parser
from mint.utils.reponse import find_success

image_bp = Blueprint("image", __name__)


@image_bp.get("/image")
def get_image():
    kw = Parser.parse_args(uid=str)
    rets, counts = ImageModel.find(**kw)
    return find_success({"image": rets[0].to_dict()})
