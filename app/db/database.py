from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

@contextmanager
def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
        db_session.commit()
    except Exception as exception:
        db_session.rollback()
        raise Exception(exception) from exception
    finally:
        db_session.close()

