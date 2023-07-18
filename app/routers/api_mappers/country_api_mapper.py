from app.routers.schemas.country_schemas import CountryCreateRequest
from app.persistence.entities import CountryEntity

class CountryApiMapper:

    def map_to_country_model(country: CountryCreateRequest)->CountryEntity:
        return CountryEntity(name=country.name, code=country.code)

