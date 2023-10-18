from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, 'pbkdf2:sha1', 16)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
