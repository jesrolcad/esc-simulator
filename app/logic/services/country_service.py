from app.persistence.repositories import country_repository
from app.logic.models import Country
from app.logic.model_mappers import country_model_mapper
from app.logic.services.base_service import BaseService
from app.persistence.repositories.country_repository import CountryRepository


class CountryService(BaseService):
    def get_country(self, id: int = None, name: str = None, code: str = None)->Country:
        country_entity = CountryRepository(self.session).get_country(id, name, code)
        return country_model_mapper.map_to_country_model(country_entity)


    def create_country(self, country: Country)->Country:
        existing_country = self.get_country(id=country.id, name=country.name, code=country.code)
        try:
            if existing_country:
                raise Exception("Country already exists")

            country_entity = country_model_mapper.map_to_country_entity(country)
            return country_model_mapper.map_to_country_model(CountryRepository(self.session).create_country(country_entity))
        
        except Exception:
            return existing_country