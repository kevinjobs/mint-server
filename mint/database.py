from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import declarative_base

from mint.constants import DBConfig

engine = create_engine(DBConfig.PATH)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

BaseModel = declarative_base()
BaseModel.query = db_session.query_property()


def init_db():
    from mint.models import FileModel
    from mint.models import PostModel
    from mint.models import UserModel
    from mint.models import ImageModel

    BaseModel.metadata.create_all(bind=engine)
