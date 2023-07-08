from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.utils.exceptions import InternalError, BusinessLogicValidationError
from app.core.config import settings 

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


def get_db():
    db_session = SessionLocal(expire_on_commit=False)
    try:
        yield db_session
        db_session.commit()
    except BusinessLogicValidationError as exception:
        db_session.rollback()
        raise BusinessLogicValidationError(str(exception))
    except InternalError as exception:
        db_session.rollback()
        raise InternalError(str(exception)) 
    finally:
        db_session.close()

