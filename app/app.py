from flask import Flask
from flask_restful import Api

from app.resources.user import UserResource
from app.resources.user import LoginResource
from app.db import db


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)

with app.app_context():
    db.create_all()

api.add_resource(UserResource, '/user')
api.add_resource(LoginResource, '/login')
