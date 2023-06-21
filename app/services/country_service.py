from app.repositories import country_repository
from app.schemas.country import CountryCreate
from app.mappers import country_mapper

def create_country(country: CountryCreate)->int:
    exists_country = country_repository.exists_country_by_name_or_code(country.name, country.code)
    if exists_country:
        raise Exception("Country already exists")
    
    country_model = country_mapper.map_to_country(country)
    return country_repository.create_country(country_model)






