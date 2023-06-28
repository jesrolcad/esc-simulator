from sqlalchemy import insert, select
from app.db.database import get_db
from app.persistence.entities import CountryEntity
from app.persistence.repositories.base_repository import BaseRepository

class CountryRepository(BaseRepository):

    def get_country(self, id: int, name: str, code: str)->CountryEntity:
        if id is None and name is None and code is None:
            raise ValueError("Id, name or code must be provided")
        query = select(CountryEntity)
        if id is not None:
            query = query.where(CountryEntity.id == id)
        elif name is not None:
            query = query.where(CountryEntity.name == name)
        elif code is not None:
            query = query.where(CountryEntity.code == code)

        return self.session.scalars(query).first()


    def create_country(self, country: CountryEntity)->CountryEntity:
            insert_stmt = (insert(CountryEntity).values(name=country.name,code=country.code).returning(CountryEntity.id))
            result = self.session.execute(insert_stmt.returning(CountryEntity.id))
            country_id = result.fetchone()[0]

            country.id = country_id
            return country
