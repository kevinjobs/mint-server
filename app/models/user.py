from werkzeug.security import generate_password_hash as gen_password
from werkzeug.security import check_password_hash
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db import db
from app.models._base import BaseModel
from app.utils import now_stamp


class UserModel(db.Model, BaseModel):
    __tablename__ = 'users'

    registerAt: Mapped[int] = mapped_column(Integer, default=now_stamp)
    updateAt: Mapped[int] = mapped_column(Integer, nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    #
    nickname: Mapped[str] = mapped_column(String, default='')
    avatar: Mapped[str] = mapped_column(String, default='')
    birthday: Mapped[str] = mapped_column(String, default='')
    gender: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, default='')
    motto: Mapped[str] = mapped_column(String, default='')
    description: Mapped[str] = mapped_column(String, default='')
    # commom, admin, superuser
    role: Mapped[str] = mapped_column(String, default='common')
    group: Mapped[str] = mapped_column(String, default='')
    #
    invitation: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.password = gen_password(self.password, 'pbkdf2:sha1', 16)

    def to_dict(self) -> dict:
        d = super().to_dict()
        if d.get('password'):
            del d['password']
        return d

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)
