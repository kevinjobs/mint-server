import os
from flask import Flask
from flask import g
from flask_restful import Api as _Api
from werkzeug.exceptions import HTTPException

from app.db import db
from app.exceptions import RestfulError
from app.utils import extract_token
from app.utils import verify_token

from app.resources.user import UserResource
from app.resources.user import LoginResource
from app.resources.file import UploadResource
from app.resources.file import DownloadResource


class Api(_Api):
    def handle_error(self, e):
        raise e


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    if isinstance(e, RestfulError):
        return e.resp()
    elif isinstance(e, HTTPException):
        return {'status': e.code, 'msg': e.description}
    else:
        raise e


@app.before_request
def load_authentication():
    """在请求前解析 token 并将信息挂在到 g 上
    """
    token = extract_token()
    payload = verify_token(token)
    if not isinstance(payload, int):
        g.user = {
            'username': payload.get('username'),
            'role': payload.get('role'),
            'group': payload.get('group')
        }


api.add_resource(UserResource, '/user')
api.add_resource(LoginResource, '/login')
api.add_resource(UploadResource, '/upload')
api.add_resource(DownloadResource, '/download')
