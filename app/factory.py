import os
from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from app.exceptions import RestfulError
from app.database import init_db
from app.database import db_session
from app.blueprints.user import user_bp
from app.blueprints.file import file_bp
from app.blueprints.auth import auth_bp
from app.blueprints.post import post_bp


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
    init_db()

    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(auth_bp)

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
