from sqlalchemy import insert, select
from app.db.database import get_db
from app.persistence.entities import CountryEntity

def get_country(id: int, name: str, code: str)->CountryEntity:
    with get_db() as db_session:
        return db_session.scalars(select(CountryEntity)
            .where(CountryEntity.id == id or CountryEntity.name == name or CountryEntity.code == code)).first()

def create_country(country: CountryEntity)->int:
    with get_db() as db_session:
        insert_stmt = (insert(CountryEntity).values(name=country.name,code=country.code).returning(CountryEntity.id))
        result = db_session.execute(insert_stmt.returning(CountryEntity.id))
        country_id = result.fetchone()[0]

        return country_id
