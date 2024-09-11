from sqlalchemy import insert, select, update, or_, and_, delete
from app.persistence.entities import CountryEntity, SongEntity
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


    def get_country_by_name_or_code(self, country_id: int, name: str, code: str)->CountryEntity:
        return self.session.scalars(select(CountryEntity).where(and_(CountryEntity.id != country_id, or_(CountryEntity.name.ilike(name), CountryEntity.code.ilike(code))))).first()

    def get_country_by_song_id(self, song_id: int)->CountryEntity:
        return self.session.scalars(select(CountryEntity).join(SongEntity).where(SongEntity.id == song_id)).first()

    def create_country(self, country: CountryEntity)->CountryEntity:
        insert_stmt = (insert(CountryEntity).values(name=country.name,code=country.code).returning(CountryEntity.id))
        result = self.session.execute(insert_stmt.returning(CountryEntity.id))
        country_id = result.fetchone()[0]

        country.id = country_id
        return country
    
    def update_country(self, country_id: int, country: CountryEntity)->CountryEntity:
        update_stmt = update(CountryEntity).where(CountryEntity.id == country_id).values(name=country.name,code=country.code)
        self.session.execute(update_stmt)

    
    def delete_country(self, country_id: int)->None:
        delete_stmt = delete(CountryEntity).where(CountryEntity.id == country_id)
        self.session.execute(delete_stmt)
