import os
import pytest
from sqlalchemy_utils import database_exists, create_database, drop_database

os.environ["ENVIRONMENT"] = "TEST"

from app.db.database import Base, engine, get_db_as_context_manager


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
    print("ENGINE URL DATABASE: ", engine.url.database)
    if(engine.url.database == os.getenv('TEST_POSTGRES_DB')):
        drop_database(engine.url)

@pytest.fixture(scope="function", autouse=True)
def after_each():
    yield
    with get_db_as_context_manager() as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())