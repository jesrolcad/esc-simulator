import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from app.utils.exceptions import InternalError, BusinessLogicValidationError
from app.core.config import dev_settings, test_settings 

environment = os.getenv("ENVIRONMENT")

Base = declarative_base()

if environment == "DEV":
    settings = dev_settings
elif environment == "TEST":
    settings = test_settings

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
        raise BusinessLogicValidationError(field=exception.field,message=str(exception))
    except InternalError as exception:
        db_session.rollback()
        raise InternalError(str(exception)) 
    finally:
        db_session.close()

@contextmanager
def get_db_as_context_manager():
    return get_db()

