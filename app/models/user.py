from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.exc import IntegrityError
from shortuuid import uuid

from app.db import db
from app.exceptions import Existed
from app.exceptions import DBError
from app.exceptions import NotFound


class UserModel(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String, unique=True, default=uuid)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    nickname: Mapped[str] = mapped_column(String, default='')
    location: Mapped[str] = mapped_column(String, default='')
    birthday: Mapped[str] = mapped_column(String, default='')
    # male or female
    gender: Mapped[str] = mapped_column(String, nullable=True)
    # commom, admin, superuser
    role: Mapped[str] = mapped_column(String, default='commom')
    group: Mapped[str] = mapped_column(String, default='')

    def __init__(self, **kw):
        self.username = kw.get('username')
        self.password = generate_password_hash(
            kw.get('password'), 'pbkdf2:sha1', 16)
        self.nickname = kw.get('nickname')
        self.location = kw.get('location')
        self.birthday = kw.get('birthday')
        self.gender = kw.get('gender')
        self.role = kw.get('role')
        self.group = kw.get('group')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            raise Existed('user [%s] existed' % self.username)
        except Exception:
            raise DBError

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'uid': self.uid,
            'nickname': self.nickname,
            'location': self.location,
            'gender': self.gender,
            'birthday': self.birthday,
            'role': self.role,
            'group': self.group,
        }

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def find_one_by_username(cls, username):
        return cls.find_by('username', username)[0]

    @classmethod
    def find_one_by_uid(cls, uid):
        return cls.find_by('uid', uid)[0]

    @classmethod
    def find_many_by_nickname(cls, nickname):
        return cls.find_by('nickname', nickname)

    @classmethod
    def find_by(cls, flag: str, value: str):
        condition = {}
        if flag == 'username':
            condition['username'] = value
        if flag == 'uid':
            condition['uid'] = value
        if flag == 'nickname':
            condition['nickname'] = value

        try:
            users = cls.query.filter_by(**condition).all()
        except Exception:
            raise DBError

        if users is None or len(users) == 0:
            items = []
            for k, v in condition.items():
                items.append('%s: %s' % (k, v))
            raise NotFound('no this user [%s]' % ', '.join(items))

        return users

    @classmethod
    def update_by_username(cls, **kw):
        try:
            user = cls.query.filter_by(username=kw['username']).first()
        except Exception:
            raise DBError

        if user is None:
            raise NotFound('no this user: [%s]' % kw['username'])

        if kw.get('username'):
            user.username = kw['username']
        if kw.get('nickname'):
            user.nickname = kw['nickname']
        if kw.get('location'):
            user.location = kw['location']
        if kw.get('birthday'):
            user.birthday = kw['birthday']
        if kw.get('gender'):
            user.gender = kw['gender']
        if kw.get('role'):
            user.role = kw['role']
        if kw.get('group'):
            user.group = kw['group']

        try:
            db.session.commit()
            return user
        except Exception:
            raise DBError

    @classmethod
    def delete_by_uid(cls, uid):
        try:
            user = cls.query.filter_by(uid=uid).first()
        except Exception:
            raise DBError

        if user is None:
            raise NotFound('no this user [%s]' % uid)

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception:
            raise DBError('delete user failed')
