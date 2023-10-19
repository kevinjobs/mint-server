from flask import Flask
from flask_restful import Api as _Api

from app.resources.user import UserResource
from app.resources.user import LoginResource
from app.db import db
from app.exceptions import RestfulError


class Api(_Api):
    def handle_error(self, e):
        raise e


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, RestfulError):
        return e.response
    if isinstance(e, Exception):
        raise e


api.add_resource(UserResource, '/user')
api.add_resource(LoginResource, '/login')
