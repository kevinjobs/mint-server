from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///mintforge.sqlite')
db_session = scoped_session(sessionmaker(
                            autocommit=False,
                            autoflush=False,
                            bind=engine))

BaseModel = declarative_base()
BaseModel.query = db_session.query_property()


def init_db():
    from mint.models import UserModel
    from mint.models import FileModel
    from mint.models import PostModel
    BaseModel.metadata.create_all(bind=engine)
