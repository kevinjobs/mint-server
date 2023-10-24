import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api as _Api
from werkzeug.exceptions import HTTPException
from app.exceptions import RestfulError
from app.database import init_db
from app.database import db_session
from app.blueprints.user import user_bp
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


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mintforge.sqlite'),
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite3',
        UPLOAD_FOLDER=os.path.join(os.getcwd(), 'upload'),
        MAX_CONTENT_LENGTH=4 * 1024 * 1024,
        STATIC_FOLDER='static',
        STATIC_URL_PATH='/static'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)
    api = Api(app)
    init_db()

    app.register_blueprint(user_bp)

    api.add_resource(LoginResource, '/login')
    api.add_resource(VerifyResource, '/verify')
    api.add_resource(InvitationResource, '/invitations')

    api.add_resource(UserResource, '/user')
    api.add_resource(UsersResource, '/users')

    api.add_resource(UploadResource, '/upload')
    api.add_resource(StaticResource, '/static/<string:filename>')

    api.add_resource(PostResource, '/p')
    api.add_resource(PostsResource, '/posts')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        if isinstance(e, RestfulError):
            return e.resp()
        elif isinstance(e, HTTPException):
            return {'status': e.code, 'msg': e.description}
        else:
            raise e

    return app
