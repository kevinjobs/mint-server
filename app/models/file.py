from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from shortuuid import uuid
import time

from app.db import db
from app.exceptions import DBError
from app.exceptions import NotFound


def now_stamp():
    return int(round(time.time() * 1000))


class FileModel(db.Model):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String, unique=True, default=uuid)
    origin: Mapped[str] = mapped_column(String, nullable=False)
    filepath: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    uploadAt: Mapped[int] = mapped_column(Integer, default=now_stamp)

    def __init__(self, **kw):
        self.origin = kw.get('origin')
        self.filepath = kw.get('filepath')
        self.filename = kw.get('filename')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise DBError(str(e))

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
