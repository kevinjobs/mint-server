from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from mint.constants import DBConfig

engine = create_engine(DBConfig.PATH)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

BaseModel = declarative_base()
BaseModel.query = db_session.query_property()


def init_db():
    from mint.models import FileModel, ImageModel, PostModel, UserModel

    BaseModel.metadata.create_all(bind=engine)
