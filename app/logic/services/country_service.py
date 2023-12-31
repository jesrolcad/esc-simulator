from app.logic.models import Country
from app.logic.model_mappers import CountryModelMapper
from app.logic.services.base_service import BaseService
from app.persistence.repositories.country_repository import CountryRepository
from app.utils.exceptions import AlreadyExistsError, NotFoundError


class CountryService(BaseService):
    def get_country(self, id: int = None, name: str = None, code: str = None)->Country:
        country_entity = CountryRepository(self.session).get_country(id, name, code)
        if country_entity is None:
            raise NotFoundError(field="country_id",message=f"Country with id {id} not found")
        return CountryModelMapper().map_to_country_model(country_entity=country_entity)
    
    def get_countries(self)->list[Country]:
        return [CountryModelMapper().map_to_country_model(country_entity=country_entity) 
                for country_entity in CountryRepository(self.session).get_countries()]

    def create_country(self, country: Country)->Country:
        self.check_country_by_name_or_code_exists(country_id=None,country=country)

        country_entity = CountryModelMapper().map_to_country_entity(country=country)
        return CountryModelMapper().map_to_country_model(CountryRepository(self.session).create_country(country=country_entity))


    def update_country(self, country_id: int, country: Country):
        existing_country = CountryRepository(self.session).get_country(id=country_id)

        if existing_country is None:
            raise NotFoundError(field="country_id",message=f"Country with id {country_id} not found")

        self.check_country_by_name_or_code_exists(country_id=country_id,country=country)

        country_entity = CountryModelMapper().map_to_country_entity(country=country)
        CountryRepository(self.session).update_country(country_id=country_id, country=country_entity)


    def check_country_by_name_or_code_exists(self, country_id: int, country: Country)->bool:
        existing_country = CountryRepository(self.session).get_country_by_name_or_code(country_id=country_id, name=country.name, code=country.code)

        if existing_country:
            raise AlreadyExistsError(field="name,code",
                message=(f"Another country with id {existing_country.id}, name {existing_country.name} " +
                        f"and code {existing_country.code} already exists. Please revise name and code"))
        

    def delete_country(self, country_id: int):
        existing_country = CountryRepository(self.session).get_country(id=country_id)

        if existing_country is None:
            raise NotFoundError(field="country_id",message=f"Country with id {country_id} not found")

        CountryRepository(self.session).delete_country(country_id=country_id)