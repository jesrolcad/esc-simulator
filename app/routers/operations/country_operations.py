import strawberry

from app.logic.models import Country
from app.logic.services.country_service import CountryService
from app.logic.services.song_service import SongService
from app.routers.api_mappers.country_api_mapper import CountryApiMapper
from app.routers.schemas.api_schemas import ResultResponseQL
from app.routers.schemas.base_schemas import BaseIdQL, BaseCountryQL
from app.routers.schemas.common_schemas import SongWithoutCountryCeremoniesVotingsQL
from app.routers.api_mappers.song_api_mapper import SongApiMapper
from app.routers.schemas.country_schemas import CountryRequestQL
from app.routers.operations.validators import validate_country_request_ql


@strawberry.type
class CountryDataResponseQL(BaseCountryQL, BaseIdQL):

    @strawberry.field
    def songs(self, info: strawberry.Info)->list[SongWithoutCountryCeremoniesVotingsQL]:
        song_models = SongService(info.context.db).get_songs_by_country_id(country_id=self.id)
        return [SongApiMapper().map_to_song_without_country_ceremonies_votings_ql(song_model=song_model) for song_model in song_models]

    @staticmethod
    def map_to_country_data_response_ql(country_model: Country)->'CountryDataResponseQL':
        return CountryDataResponseQL(id=country_model.id, name=country_model.name, code=country_model.code)

@strawberry.type
class CountryQuery:
    @strawberry.field
    def country(self, info: strawberry.Info, country_id: int)->CountryDataResponseQL:
        response = CountryService(info.context.db).get_country(id=country_id, submodels=False)
        return CountryDataResponseQL.map_to_country_data_response_ql(response)

    @strawberry.field
    def countries(self, info: strawberry.Info)->list[CountryDataResponseQL]:
        response = CountryService(info.context.db).get_countries(submodels=False)
        return [CountryDataResponseQL.map_to_country_data_response_ql(country) for country in response]


@strawberry.type
class CountryMutation:
    @strawberry.mutation
    def create_country(self, info: strawberry.Info, country: CountryRequestQL)->CountryDataResponseQL:
        validate_country_request_ql(country=country)
        country_model = CountryApiMapper().map_country_request_ql_to_country_model(country_schema_ql=country)
        country = CountryService(info.context.db).create_country(country=country_model)
        return CountryDataResponseQL.map_to_country_data_response_ql(country)

    @strawberry.mutation
    def update_country(self, info: strawberry.Info, country_id: int, country: CountryRequestQL)->ResultResponseQL:
        validate_country_request_ql(country=country)
        country_model = CountryApiMapper().map_country_request_ql_to_country_model(country_schema_ql=country)
        CountryService(info.context.db).update_country(country_id=country_id, country=country_model)
        return ResultResponseQL(success=True, message=f"Country with id {country_id} updated successfully")


    @strawberry.mutation
    def delete_country(self, info: strawberry.Info, country_id: int)->ResultResponseQL:
        CountryService(info.context.db).delete_country(country_id=country_id)
        return ResultResponseQL(success=True, message=f"Country with id {country_id} deleted successfully")