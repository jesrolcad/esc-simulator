from app.persistence.repositories import country_repository
from app.logic.models.country import Country
from app.logic.model_mappers import country_model_mapper

def create_country(country: Country)->int:
    country_entity = country_model_mapper.map_to_country_entity(country)
    return country_repository.create_country(country_entity)


def get_country(id: int = None, name: str = None, code: str = None)->Country:
    country_entity = country_repository.get_country(id, name, code)
    return country_model_mapper.map_to_country_model(country_entity)
