from app.persistence.repositories import country_repository
from app.logic.models.country import Country
from app.logic.model_mappers import country_model_mapper

def create_country(country: Country)->int:
    exists_country = country_repository.get_country_by_name_or_code(country.name, country.code)
    if exists_country:
        raise Exception("Country already exists")

    country_entity = country_model_mapper.map_to_country_entity(country)
    return country_repository.create_country(country_entity)

def exists_country_by_name_or_code(name: str = "", code: str = "")->bool:
    return country_repository.get_country_by_name_or_code(name, code)
