from app.routers.schemas.country_schemas import CountryRequest
from app.persistence.entities import CountryEntity
from app.logic.models import Country
from app.routers.schemas.country_schemas import CountryDataResponse

class CountryApiMapper:

    def map_to_country_model(self, country: CountryRequest)->CountryEntity:
        return CountryEntity(name=country.name, code=country.code)
    
    def map_to_country_data_response(self, country_model: Country)->CountryDataResponse:
        return CountryDataResponse(id=country_model.id, name=country_model.name, code=country_model.code, 
                                songs=[song.__dict__ for song in country_model.songs])


