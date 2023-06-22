from app.routers.schemas.country import CountryCreateRequest
from app.persistence.entities import Country

def map_to_country_model(country: CountryCreateRequest)->Country:
    return Country(name=country.name, code=country.code)

