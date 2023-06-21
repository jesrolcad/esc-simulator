from app.db.database import get_db
from app.db.models import Country

from sqlalchemy import insert, select

def exists_country_by_name_or_code(name: str = "", code: str = "")->bool:
    with get_db() as db:
        return db.scalars(select(Country).where(Country.name == name or Country.code == code)).first() is not None


def create_country(country: Country)->int:
    with get_db() as db:
        insert_stmt = insert(Country).values(name=country.name, code=country.code).returning(Country.id)
        result = db.execute(insert_stmt.returning(Country.id))
        country_id = result.fetchone()[0]
        return country_id

