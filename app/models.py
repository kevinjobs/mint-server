from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from shortuuid import uuid

from app.database import BaseModel
from app.database import db_session
from app.utils import now_stamp
from app.exceptions import DBError
from app.exceptions import Existed
from app.exceptions import NotFound


class Base(object):
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, default=uuid)
    updateAt = Column(Integer, nullable=True)
    createAt = Column(Integer, default=now_stamp)

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def save(self):
        """save the model instace to database

        Raises:
            DBError: Database Error
        """
        try:
            db_session.add(self)
            db_session.commit()
            return
        except IntegrityError as e:
            if e.code == 'gkpj':
                raise Existed
            else:
                raise DBError(str(e))
        except Exception as e:
            raise DBError(str(e))

    def to_dict(self) -> dict:
        d = {}
        for attr, value in self.__dict__.items():
            if not attr.startswith('_sa_instance'):
                d[attr] = value
        return d

    @classmethod
    def find(cls, **kw):
        kw = cls.purge_kw(kw)
        offset = kw.get('offset')
        limit = kw.get('limit')
        if offset is not None:
            del kw['offset']
        else:
            offset = 0

        if limit is not None:
            del kw['limit']
        else:
            limit = 10

        try:
            rets = cls.query.filter_by(**kw) \
                .order_by(-cls.createAt).offset(offset).limit(limit).all()
        except Exception as e:
            raise DBError(str(e))

        if rets is None or len(rets) == 0:
            raise NotFound('cannot find: [%s]' % cls.concat_kw(kw))

        return rets

    @classmethod
    def find_by_uid(cls, uid: str):
        return cls.find(uid=uid)[0]

    @classmethod
    def delete_by_uid(cls, uid: str):
        ret = cls.find_by_uid(uid)

        try:
            db_session.delete(ret)
            db_session.commit()
        except Exception:
            raise DBError('delete [%s] failed' % uid)

    @classmethod
    def update(cls, **kw):
        kw = cls.purge_kw(kw)
        ret = cls.find_by_uid(kw.get('uid'))

        for k, v in kw.items():
            setattr(ret, k, v)

        if hasattr(ret, 'updateAt'):
            ret.updateAt = now_stamp()

        try:
            db_session.commit()
            return ret
        except Exception:
            raise DBError

    @staticmethod
    def concat_kw(kw: dict):
        arr = []
        for k, v in kw.items():
            s = '{}:{}'.format(k, v)
            arr.append(s)
        return ','.join(arr)

    @staticmethod
    def purge_kw(kw: dict):
        kws = {**kw}
        for k, v in kws.items():
            if v is None:
                del kw[k]
        return kw


class UserModel(BaseModel, Base):
    __tablename__ = 'users'

    registerAt = Column(Integer, default=now_stamp)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    #
    nickname = Column(String, default='')
    avatar = Column(String, default='')
    birthday = Column(String, default='')
    gender = Column(String, nullable=True)
    location = Column(String, default='')
    motto = Column(String, default='')
    description = Column(String, default='')
    # commom, admin, superuser
    role = Column(String, default='common')
    group = Column(String, default='')
    #
    invitation = Column(String, nullable=False)


class FileModel(BaseModel, Base):
    __tablename__ = 'files'

    origin = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    uploadAt = Column(Integer, default=now_stamp)

    def __init__(self, **kw):
        self.origin = kw.get('origin')
        self.filepath = kw.get('filepath')
        self.filename = kw.get('filename')

    def to_dict(self):
        return {
            'origin': self.origin,
            'filepath': self.filepath,
            'filename': self.filename,
        }

    @classmethod
    def find_by_filename(cls, filename: str):
        try:
            file: FileModel = cls.query.filter_by(filename=filename).first()
        except Exception:
            raise DBError

        if not file:
            raise NotFound

        return file


class PostModel(BaseModel, Base):
    __tablename__ = 'posts'

    createAt = Column(Integer, default=now_stamp)
    publishAt = Column(Integer, nullable=True)
    updateAt = Column(Integer, nullable=True)
    # post type: article, photo, etc..
    type = Column(String, default='article')

    title = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=False)
    content = Column(String, default='')
    excerpt = Column(String, nullable='')

    cover = Column(String, nullable=True)
    status = Column(String, default='draft')
    tags = Column(String, default='')
    category = Column(String, default='')
    format = Column(String, default='plain')

    url = Column(String, default='')
    exif = Column(String, default='')
    description = Column(String, default='')