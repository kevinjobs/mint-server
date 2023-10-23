import os
from flask import Flask
from flask_restful import Api as _Api
from flask_cors import CORS
# from datetime import timedelta
from werkzeug.exceptions import HTTPException

from app.db import db
from app.exceptions import RestfulError

from app.resources.auth import LoginResource
from app.resources.auth import VerifyResource
from app.resources.auth import InvitationResource

from app.resources.user import UserResource
from app.resources.user import UsersResource
from app.resources.file import UploadResource
from app.resources.file import StaticResource
from app.resources.post import PostResource
from app.resources.post import PostsResource


class Api(_Api):
    def handle_error(self, e):
        raise e


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['STATIC_FOLDER'] = 'uploads'
app.config['STATIC_URL_PATH'] = '/static'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

db.init_app(app)
cors = CORS(app)
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


api.add_resource(LoginResource, '/login')
api.add_resource(VerifyResource, '/verify')
api.add_resource(InvitationResource, '/invitations')

api.add_resource(UserResource, '/user')
api.add_resource(UsersResource, '/users')

api.add_resource(UploadResource, '/upload')
api.add_resource(StaticResource, '/static/<string:filename>')

api.add_resource(PostResource, '/p')
api.add_resource(PostsResource, '/posts')
