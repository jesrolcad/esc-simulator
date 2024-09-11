import strawberry
from app.logic.services.song_service import SongService
from app.logic.services.country_service import CountryService
from app.routers.api_mappers.country_api_mapper import CountryApiMapper
from app.routers.api_mappers.song_api_mapper import SongApiMapper
from app.routers.schemas.base_schemas import BaseIdQL, BaseSongQL, ScoreEnum
from app.routers.schemas.common_schemas import CountryWithoutSongsVotingsDataResponseQL
from app.logic.models import Song


@strawberry.type
class SongDataResponseQL(BaseSongQL, BaseIdQL):
    _country: strawberry.Private[CountryWithoutSongsVotingsDataResponseQL] = None

    @strawberry.field
    def country(self, info: strawberry.Info) -> CountryWithoutSongsVotingsDataResponseQL:
        country_model =  CountryService(info.context.db).get_country_by_song_id(song_id=self.id)
        country_ql_schema = CountryApiMapper().map_to_country_without_songs_votings_data_response_ql(country_model=country_model)
        self._country = country_ql_schema

        return country_ql_schema
    
    @strawberry.field
    def summary(self, info: strawberry.Info) -> str:
        country_name = self._country.name if self._country else None 

        return SongService(info.context.db).get_song_summary(song_id=self.id, title=self.title, artist=self.artist, country_name=country_name) # We have to pass country somehow
    
    @staticmethod
    def map_to_song_data_response_ql(song_model: Song)->'SongDataResponseQL':
        return SongDataResponseQL(id=song_model.id, title=song_model.title, artist=song_model.artist,
                                  belongs_to_host_country=song_model.belongs_to_host_country,
                                  jury_potential_score=ScoreEnum(song_model.jury_potential_score).value,
                                  televote_potential_score=ScoreEnum(song_model.televote_potential_score).value)

@strawberry.type
class SongQuery:
    @strawberry.field
    def songs(self, info: strawberry.Info, title: str | None = None, country_code: str | None = None, event_year: int | None = None) -> list[SongDataResponseQL]:
        response = SongService(info.context.db).get_songs(title=title, country_code=country_code, event_year=event_year)
        return [SongDataResponseQL.map_to_song_data_response_ql(song) for song in response]


    @strawberry.field
    def song(self, song_id: int, info: strawberry.Info) -> SongDataResponseQL:
        response = SongService(info.context.db).get_song(song_id)
        return SongDataResponseQL.map_to_song_data_response_ql(response)