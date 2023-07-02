from app.routers.schemas.country_schemas import CountryCreateRequest
from app.persistence.entities import CountryEntity

def map_to_country_model(country: CountryCreateRequest)->CountryEntity:
    return CountryEntity(name=country.name, code=country.code)

