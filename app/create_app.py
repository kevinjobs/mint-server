import os

from flask import Flask
from app.db import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mintforge.sqlite'),
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite3',
        UPLOAD_FOLDER=os.path.join(os.getcwd(), 'upload'),
        MAX_CONTENT_LENGTH=4*1024*1024,
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

    db.init_app(app)

    return app
