import os
import json
import time

import cv2
from shortuuid import uuid

from mint.constants import FilePath


def compress_image(orgin: str, output: str):
    """压缩图片

    Args:
        orgin (str): 原始路径
        output (str): 输出路径
    """
    img = cv2.imread(orgin)
    x, y = img.shape[0:2]
    width = 300
    height = int(y / (x / width))
    img2 = cv2.resize(img, (height, width), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(output, img2)


def read_image_wh(p: str):
    img = cv2.imread(p)
    x, y = img.shape[0:2]
    return y, x


def ensure_path(path: str):
    """ensure the path exists

    Args:
        path (str): pathlike
    """
    if not os.path.exists(path):
        os.makedirs(path)


def now_stamp():
    return int(round(time.time() * 1000))


def check_invitation(c: str):
    from mint.exceptions import InvalidInvitation

    codes = open_invitation()

    i = 0
    for invi in codes:
        if invi["code"] == c and invi["valid"]:
            return True
        i += 1

    raise InvalidInvitation("邀请码无效或者已经被使用")


def invalidate_invitation(c: str, username=None):
    codes = open_invitation()

    i = 0
    for invi in codes:
        if invi["code"] == c:
            codes[i]["valid"] = False
            codes[i]["registerAt"] = now_stamp()
            codes[i]["registerBy"] = username if username else ""
            with open(FilePath.INVITATION_FILE, "w") as fp:
                json.dump(codes, fp, ensure_ascii=False, indent=2)
            return True
        i += 1


def gen_invitation(counts=10):
    codes = []
    datas = open_invitation()
    for _ in range(0, counts):
        codes.append(
            {
                "createAt": now_stamp(),
                "code": uuid(),
                "valid": True,
            }
        )

    with open(FilePath.INVITATION_FILE, "w") as fp:
        json.dump(codes + datas, fp, ensure_ascii=False, indent=2)


def open_invitation():
    try:
        with open(FilePath.INVITATION_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
