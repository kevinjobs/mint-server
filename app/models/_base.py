from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.exc import IntegrityError
from shortuuid import uuid

from app.db import db
from app.exceptions import DBError
from app.exceptions import Existed
from app.exceptions import NotFound
from app.utils import now_stamp


class BaseModel(object):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String, unique=True, default=uuid)

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def save(self):
        """save the model instace to database

        Raises:
            DBError: Database Error
        """
        try:
            db.session.add(self)
            db.session.commit()
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
            db.session.delete(ret)
            db.session.commit()
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
            db.session.commit()
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
