from app.logic.models import Country
from app.persistence.entities import CountryEntity


class CountryModelMapper:

    def map_to_country_entity(self, country: Country)->CountryEntity:
        return CountryEntity(id=country.id, name=country.name, code=country.code)


    def map_to_country_model(self, country_entity: CountryEntity)->Country:
        if country_entity is None:
            return None
        return Country(id=country_entity.id, name=country_entity.name, code=country_entity.code)
