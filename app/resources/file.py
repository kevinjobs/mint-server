import os
from flask_restful import Resource
from flask_restful import reqparse
from flask import request
from flask import send_from_directory
from shortuuid import uuid

from app.utils import response
from app.utils import RespCode
from app.utils import RespMsg
from app.utils import ensure_path
from app.exceptions import NotAllowed
from app.models.file import FileModel


IMG_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
AUDIO_EXTENSIONS = ['mp3', 'flac', 'ape', 'm4a']
DOC_EXTENSIONS = ['txt', 'ppt', 'doc', 'xls', 'pptx', 'xlsx', 'docx', 'pdf']
ALLOWED_EXTENSIONS = IMG_EXTENSIONS + AUDIO_EXTENSIONS + DOC_EXTENSIONS


class UploadResource(Resource):
    def post(self):
        """upload a file to server

        Raises:
            NotAllowed: the file with the extension is not allowed to upload

        Returns:
            json: response in json

        Usage:
            url: /upload
            body: form-data
        """
        from app.app import app
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
        url = '/download?filename=' + filename
        # 判断是否为允许上传的文件类型
        # to-do: 应当根据文件的实际类型来判断
        if ext not in ALLOWED_EXTENSIONS:
            raise NotAllowed('文件格式[%s]不被支持' % ext)

        # 根据不同的文件类型，保存到对应的文件夹
        pathname = ''
        if ext in IMG_EXTENSIONS:
            pathname = os.path.join('img')
        if ext in AUDIO_EXTENSIONS:
            pathname = os.path.join('audio')
        if ext in DOC_EXTENSIONS:
            pathname = os.path.join('doc')
        # 如果文件夹不存在，则创建
        ensure_path(os.path.join(upload_path, pathname))
        # 保存文件
        file.save(os.path.join(upload_path, pathname, filename))
        # 创建一个数据库对象
        file_model = FileModel(
            origin=origin,
            filepath=pathname,
            filename=filename
        )
        # 保存文件信息到数据库
        file_model.save()

        return response(RespCode.OK, RespMsg.OK, {
            'filename': filename,
            'origin': origin,
            'url': url,
        })


class DownloadResource(Resource):
    def get(self):
        """download file from server

        Returns:
            bytes: file binary in types

        Usage:
            url: /download?filename=xxx
        """
        from app.app import app
        upload_path = app.config['UPLOAD_FOLDER']
        # 解析参数 filename
        parser = reqparse.RequestParser()
        parser.add_argument('filename', type=str, location='args')
        args = parser.parse_args()
        filename = args.get('filename')
        # 从数据库中查找文件信息
        file = FileModel.find_by_filename(filename)
        # 获取文件路径
        filepath = os.path.join(upload_path, file.filepath)
        # 使用自带函数传输文件到客户端
        return send_from_directory(filepath, filename)
