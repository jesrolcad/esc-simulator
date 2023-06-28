from app.persistence.repositories import country_repository
from app.logic.models import Country
from app.logic.model_mappers import country_model_mapper


class CountryService:
    

def get_country(id: int = None, name: str = None, code: str = None)->Country:
    country_entity = country_repository.get_country(id, name, code)
    return country_model_mapper.map_to_country_model(country_entity)


def create_country(country: Country)->Country:
    existing_country = get_country(id=country.id, name=country.name, code=country.code)
    try:
        if existing_country:
            raise Exception("Country already exists")

        country_entity = country_model_mapper.map_to_country_entity(country)
        return country_model_mapper.map_to_country_model(country_repository.create_country(country_entity))
    
    except Exception:
        return existing_country