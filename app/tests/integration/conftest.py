import os
import pytest
from sqlalchemy_utils import database_exists, create_database, drop_database
os.environ["ENVIRONMENT"] = "TEST"
from app.db.database import Base, engine


def import_db_entities():
    from app.persistence.entities import CountryEntity, SongEntity, EventEntity, CeremonyEntity, \
    CeremonyTypeEntity, VotingEntity, VotingTypeEntity


@pytest.fixture(scope="session", autouse=True)
def before_all():
    if not database_exists(engine.url):
        create_database(engine.url)
        import_db_entities()
        Base.metadata.create_all(engine)



@pytest.fixture(scope="session", autouse=True)
def after_all():
    yield
    drop_database(engine.url)



@pytest.fixture(scope="function", autouse=True)
def after_each():
    yield
    Base.metadata.drop_all(engine)