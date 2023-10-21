from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.db import db
from app.models._base import BaseModel
from app.utils import now_stamp


class PostModel(db.Model, BaseModel):
    __tablename__ = 'posts'

    createAt: Mapped[int] = mapped_column(Integer, default=now_stamp)
    publishAt: Mapped[int] = mapped_column(Integer, nullable=True)
    updateAt: Mapped[int] = mapped_column(Integer, nullable=True)
    # post type: article, photo, etc..
    type: Mapped[str] = mapped_column(String, default='article')

    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, default='')
    excerpt: Mapped[str] = mapped_column(String, nullable='')

    cover: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default='draft')
    tags: Mapped[str] = mapped_column(String, default='')
    category: Mapped[str] = mapped_column(String, default='')
    format: Mapped[str] = mapped_column(String, default='plain')

    url: Mapped[str] = mapped_column(String, default='')
    exif: Mapped[str] = mapped_column(String, default='')
    description: Mapped[str] = mapped_column(String, default='')
