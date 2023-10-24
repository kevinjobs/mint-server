from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flask_restful import Api as _Api
from app.create_app import create_app
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
from app.database import init_db
from app.database import db_session


class Api(_Api):
    def handle_error(self, e):
        raise e


app = create_app()
CORS(app)
api = Api(app)
init_db()


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


api.add_resource(LoginResource, '/login')
api.add_resource(VerifyResource, '/verify')
api.add_resource(InvitationResource, '/invitations')

api.add_resource(UserResource, '/user')
api.add_resource(UsersResource, '/users')

api.add_resource(UploadResource, '/upload')
api.add_resource(StaticResource, '/static/<string:filename>')

api.add_resource(PostResource, '/p')
api.add_resource(PostsResource, '/posts')
