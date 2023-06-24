from app.logic.models.country import Country
from app.persistence.entities import CountryEntity

def map_to_country_entity(country: Country)->CountryEntity:
    return CountryEntity(id=country.id, name=country.name, code=country.code)


def map_to_country_model(country_entity: CountryEntity)->Country:
    return Country(id=country_entity.id, name=country_entity.name, code=country_entity.code)
