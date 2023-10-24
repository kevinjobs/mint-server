from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///test.db')
db_session = scoped_session(sessionmaker(
                            autocommit=False,
                            autoflush=False,
                            bind=engine))

BaseModel = declarative_base()
BaseModel.query = db_session.query_property()


def init_db():
    from app.models import UserModel
    from app.models import FileModel
    from app.models import PostModel
    BaseModel.metadata.create_all(bind=engine)