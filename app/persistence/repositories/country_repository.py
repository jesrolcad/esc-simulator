from app.db.database import get_db
from app.persistence.entities import CountryEntity

from sqlalchemy import insert, select

def exists_country_by_name_or_code(name: str = "", code: str = "")->bool:
    with get_db() as db:
        return db.scalars(select([1]).where(CountryEntity.name == name or CountryEntity.code == code)).first() is not None


def create_country(country: CountryEntity)->int:
    with get_db() as db:
        insert_stmt = insert(CountryEntity).values(name=country.name, code=country.code).returning(CountryEntity.id)
        result = db.execute(insert_stmt.returning(CountryEntity.id))
        country_id = result.fetchone()[0]
        return country_id

