from shortuuid import uuid
from sqlalchemy import Column, Float, ForeignKey, Integer, String, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash as check_password
from werkzeug.security import generate_password_hash as gen_password

from mint.database import BaseModel, db_session
from mint.exceptions import DBError, Existed, NotFound
from mint.utils import now_stamp


class Base(object):
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, default=uuid)
    updateAt = Column(Integer, nullable=True)
    createAt = Column(Integer, default=now_stamp)
    deleteAt = Column(Integer, nullable=True)

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
            if e.code == "gkpj":
                col = str(e).split("\n")[0].split(":")[1].strip()
                raise Existed(f"存在相同的字段:[{col}],该字段不能重复")
            else:
                raise DBError(str(e))
        except Exception as e:
            raise DBError(str(e))

    def to_dict(self) -> dict:
        d = {}
        for attr, value in self.__dict__.items():
            if not attr.startswith("_sa_instance"):
                d[attr] = value

        try:
            del d["deleteAt"]
        except KeyError:
            pass

        return d

    @classmethod
    def find(cls, **kw):
        kw = cls.purge_kw(kw)
        offset = kw.get("offset")
        limit = kw.get("limit")

        if offset is not None:
            del kw["offset"]
        else:
            offset = 0

        if limit is not None:
            del kw["limit"]
        else:
            limit = 10

        kw["deleteAt"] = None

        try:
            counts = db_session.query(func.count(cls.id)).filter_by(**kw).scalar()

            rets = cls.query.filter_by(**kw).order_by(-cls.createAt).offset(offset).limit(limit).all()
        except Exception as e:
            raise DBError(str(e))

        if rets is None or len(rets) == 0:
            raise NotFound("cannot find: [%s]" % cls.concat_kw(kw))

        return rets, counts

    @classmethod
    def find_by_uid(cls, uid: str):
        ret, counts = cls.find(uid=uid)
        return ret[0]

    @classmethod
    def delete_by_uid(cls, uid: str):
        ret = cls.find_by_uid(uid)
        ret.deleteAt = now_stamp()
        try:
            # db_session.delete(ret)
            db_session.commit()
        except Exception:
            raise DBError("delete [%s] failed" % uid)

    @classmethod
    def update(cls, **kw):
        kw = cls.purge_kw(kw)
        ret = cls.find_by_uid(kw.get("uid"))

        for k, v in kw.items():
            setattr(ret, k, v)

        if hasattr(ret, "updateAt"):
            ret.updateAt = now_stamp()

        try:
            db_session.commit()
            return ret
        except Exception as e:
            raise DBError(str(e))

    @staticmethod
    def concat_kw(kw: dict):
        arr = []
        for k, v in kw.items():
            s = "{}:{}".format(k, v)
            arr.append(s)
        return ",".join(arr)

    @staticmethod
    def purge_kw(kw: dict):
        """
        从给定的字典中删除值为None或"all"的键值对。

        Args:
            kw (dict): 待处理的字典。

        Returns:
            dict: 删除了值为None或"all"的键值对后的字典。

        """
        kws = {**kw}
        for k, v in kws.items():
            if v is None or v == "all":
                del kw[k]
        return kw


class UserModel(BaseModel, Base):
    __tablename__ = "users"

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    #
    nickname = Column(String, default="")
    avatar = Column(String, default="")
    birthday = Column(String, default="")
    gender = Column(String, nullable=True)
    location = Column(String, default="")
    motto = Column(String, default="")
    description = Column(String, default="")
    # commom, admin, superuser
    role = Column(String, default="common")
    group = Column(String, default="")
    #
    invitation = Column(String, nullable=False)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.password = gen_password(self.password, "pbkdf2:sha1", 16)

    def to_dict(self) -> dict:
        d = super().to_dict()
        if d.get("password"):
            del d["password"]
        return d

    def check_password(self, password) -> bool:
        return check_password(self.password, password)

    @classmethod
    def update(cls, **kw) -> None:
        password = kw.get("password")
        if password:
            kw["password"] = gen_password(password, "pbkdf2:sha1", 16)
        super().update(**kw)


class FileModel(BaseModel, Base):
    __tablename__ = "files"

    origin = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    filename = Column(String, nullable=False)

    def __init__(self, **kw):
        self.origin = kw.get("origin")
        self.filepath = kw.get("filepath")
        self.filename = kw.get("filename")

    def to_dict(self):
        return {
            "origin": self.origin,
            "filepath": self.filepath,
            "filename": self.filename,
        }

    @classmethod
    def delete_by_filename(cls, filename: str):
        rets, counts = cls.find(filename=filename)
        rets[0].deleteAt = now_stamp()
        try:
            db_session.commit()
        except Exception:
            raise DBError("delete [%s] failed" % filename)

    @classmethod
    def find_by_filename(cls, filename: str):
        try:
            file: FileModel = cls.query.filter_by(filename=filename, deleteAt=None).first()
        except Exception:
            raise DBError

        if not file:
            raise NotFound

        return file


class PostModel(BaseModel, Base):
    __tablename__ = "posts"

    # post type: article, photo, etc..
    type = Column(String, default="article")

    title = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=False)
    content = Column(String, default="")
    excerpt = Column(String, default="")
    description = Column(String, default="")

    # cover = Column(String, nullable=True)
    status = Column(String, default="draft")
    tags = Column(String, default="")
    category = Column(String, default="")
    format = Column(String, default="plain")

    #
    image = relationship("ImageModel", backref="posts")
    image_uid = Column(String, ForeignKey("images.uid"))

    def to_dict(self):
        d = super().to_dict()
        d["image"] = self.image.to_dict() if self.image else {}
        return d


class ImageModel(BaseModel, Base):
    __tablename__ = "images"

    title = Column(String)
    author = Column(String)
    description = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    #
    latitude = Column(Float)
    longitude = Column(Float)
    latitudeRef = Column(String)
    longitudeRef = Column(String)
    altitude = Column(String)
    altitudeRef = Column(String)
    #
    aperture = Column(String)
    focalLength = Column(String)
    iso = Column(Integer)
    exposure = Column(String)
    lens = Column(String)
    model = Column(String)
    #
    uri = Column(String, unique=True)

    #
    def to_dict(self):
        d = super().to_dict()
        d["posts"] = [post.uid for post in self.posts]
        return d
