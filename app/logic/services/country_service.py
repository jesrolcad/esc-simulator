from app.persistence.repositories import country_repository
from app.logic.models.country import Country
from app.logic.model_mappers import country_model_mapper

def create_country(country: Country)->int:
    exists_country = country_repository.exists_country_by_name_or_code(country.name, country.code)
    if exists_country:
        raise Exception("Country already exists")
    
    country_entity = country_model_mapper.map_to_country_entity(country)
    return country_repository.create_country(country_entity)






