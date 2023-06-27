from sqlalchemy import insert, select
from app.db.database import get_db
from app.persistence.entities import CountryEntity

def get_country(id: int, name: str, code: str)->CountryEntity:
    if id is None and name is None and code is None:
        raise ValueError("Id, name or code must be provided")
    with get_db() as db_session:
        query = select(CountryEntity)
        if id is not None:
            query = query.where(CountryEntity.id == id)
        elif name is not None:
            query = query.where(CountryEntity.name == name)
        elif code is not None:
            query = query.where(CountryEntity.code == code)
        return db_session.scalars(query).first()


def create_country(country: CountryEntity)->CountryEntity:
    with get_db() as db_session:
        insert_stmt = (insert(CountryEntity).values(name=country.name,code=country.code).returning(CountryEntity.id))
        result = db_session.execute(insert_stmt.returning(CountryEntity.id))
        country_id = result.fetchone()[0]

        country.id = country_id
        return country
