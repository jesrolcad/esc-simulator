from sqlalchemy import insert, select, update, or_
from app.persistence.entities import CountryEntity
from app.persistence.repositories.base_repository import BaseRepository

class CountryRepository(BaseRepository):

    def get_countries(self)->CountryEntity:
        return self.session.scalars(select(CountryEntity)).all()


    def get_country(self, id: int = None, name: str = None, code: str = None)->CountryEntity:
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


    def get_country_by_name_or_code(self, name: str, code: str)->CountryEntity:
        return self.session.scalars(select(CountryEntity).where(or_(CountryEntity.name.ilike(name), CountryEntity.code.ilike(code)))).first()


    def create_country(self, country: CountryEntity)->CountryEntity:
        insert_stmt = (insert(CountryEntity).values(name=country.name,code=country.code).returning(CountryEntity.id))
        result = self.session.execute(insert_stmt.returning(CountryEntity.id))
        country_id = result.fetchone()[0]

        country.id = country_id
        return country
    
    def update_country(self, country_id: int, country: CountryEntity)->CountryEntity:
        update_stmt = update(CountryEntity).where(CountryEntity.id == country_id).values(name=country.name,code=country.code)
        self.session.execute(update_stmt)
