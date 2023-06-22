from app.logic.models.country import Country
from app.persistence.entities import CountryEntity

def map_to_country_entity(country: Country)->CountryEntity:
    return CountryEntity(id=country.id, name=country.name, code=country.code)


