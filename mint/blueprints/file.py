import os
from flask import Blueprint
from flask import request
from flask import current_app as app
from flask import send_from_directory
from shortuuid import uuid
from mint.models import FileModel
from mint.utils import ensure_path
from mint.utils import compress_image
from mint.utils import read_image_wh
from mint.utils.reponse import response
from mint.utils.reponse import find_success
from mint.utils.reponse import del_success
from mint.utils.auth import PermCheck
from mint.utils.parser import Parser
from mint.exceptions import NotAllowed


IMG_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
AUDIO_EXTENSIONS = ['mp3', 'flac', 'ape', 'm4a']
DOC_EXTENSIONS = ['txt', 'ppt', 'doc', 'xls', 'pptx', 'xlsx', 'docx', 'pdf']
ALLOWED_EXTENSIONS = IMG_EXTENSIONS + AUDIO_EXTENSIONS + DOC_EXTENSIONS


file_bp = Blueprint('file', __name__)


@file_bp.post('/upload')
def upload_file():
    """upload a file to server

    Raises:
        NotAllowed: the file with the extension is not allowed to upload

    Returns:
        json: response in json

    Usage:
        url: /upload
        body: form-data
    """
    # 注册用户以上可以上传文件
    PermCheck.common_above()
    upload_path = app.config['UPLOAD_FOLDER']
    # 解析文件体
    file = request.files['file']
    # 原文件名
    origin = file.filename
    # 拓展名
    ext = file.filename.split('.')[-1]
    # 重命名，以防止不安全的文件名
    filename = '%s.%s' % (uuid(), ext)
    # 构建下载路径
    url = app.config['STATIC_URL_PATH'] + '/' + filename
    # 判断是否为允许上传的文件类型
    # to-do: 应当根据文件的实际类型来判断
    if ext not in ALLOWED_EXTENSIONS:
        raise NotAllowed('文件格式[%s]不被支持' % ext)

    # 根据不同的文件类型，保存到对应的文件夹
    filetype = ''
    if ext in IMG_EXTENSIONS:
        filetype = 'img'
    if ext in AUDIO_EXTENSIONS:
        filetype = 'audio'
    if ext in DOC_EXTENSIONS:
        filetype = 'doc'

    save_dir = os.path.join(upload_path, filetype)
    # 如果文件夹不存在，则创建
    ensure_path(save_dir)
    # 保存文件
    save_path = os.path.join(save_dir, filename)
    file.save(save_path)

    if ext in IMG_EXTENSIONS:
        w, h = read_image_wh(save_path)
    else:
        w, h = 0, 0

    # 如果是图片则进行压缩
    if ext in IMG_EXTENSIONS:
        compress_dir = os.path.join(upload_path, filetype + '-thumb')
        ensure_path(compress_dir)
        compress_path = os.path.join(compress_dir, 'thumb-' + filename)
        compress_image(save_path, compress_path)

    # 创建一个数据库对象
    file_model = FileModel(
        origin=origin,
        filepath=filetype,
        filename=filename
    )
    # 保存文件信息到数据库
    file_model.save()

    return response(0, '上传文件成功', {
        'filename': filename,
        'origin': origin,
        'url': url,
        'width': w,
        'height': h,
        'ext': ext
    })


@file_bp.get('/static/<filename>')
def get(filename: str):
    """download file from server

    Returns:
        bytes: file binary in types

    Usage:
        url: /static/<filename>
    """
    # 普通用户即可请求静态文件
    upload_path = app.config['UPLOAD_FOLDER']
    origin_filename = filename
    filename = filename.replace('thumb-', '')

    # 从数据库中查找文件信息
    file = FileModel.find_by_filename(filename)
    # 获取文件路径
    filepath = os.path.join(upload_path, file.filepath)

    # 以 thumb 开头的，获取缩略图返回
    if origin_filename.startswith('thumb-'):
        filepath = os.path.join(upload_path, file.filepath + '-thumb')
        # 使用自带函数传输文件到客户端
        return send_from_directory(filepath, origin_filename)

    return send_from_directory(filepath, filename)


@file_bp.get('/file/list')
def get_file_list():
    # 只有超级用户才可以查看后台文件列表
    PermCheck.is_superuser()
    args = {}
    args['offset'] = int
    args['limit'] = int
    kw = Parser.parse_args(**args)
    files, counts = FileModel.find(**kw)
    return find_success({
        'totals': counts,
        'amount': len(files),
        'offset': kw.get('offset') or 0,
        'limit': kw.get('limit') or 10,
        'files': [file.to_dict() for file in files]
    })


@file_bp.delete('/file')
def delete_a_file():
    # 只有超级用户才可以删除文件
    PermCheck.is_superuser()
    filename = Parser.parse_args(filename=str).get('filename')
    FileModel.delete_by_filename(filename)
    return del_success()
