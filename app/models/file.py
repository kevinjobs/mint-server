from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db import db
from app.exceptions import DBError
from app.exceptions import NotFound
from app.models._base import BaseModel
from app.utils import now_stamp


class FileModel(db.Model, BaseModel):
    __tablename__ = 'files'

    origin: Mapped[str] = mapped_column(String, nullable=False)
    filepath: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    uploadAt: Mapped[int] = mapped_column(Integer, default=now_stamp)

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
