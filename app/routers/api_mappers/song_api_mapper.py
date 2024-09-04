from app.logic.models import Song, Event, Country
from app.routers.api_mappers.country_api_mapper import CountryApiMapper
from app.routers.schemas.base_schemas import ScoreEnum
from app.routers.schemas.song_schemas import SongDataResponse, SongDataResponseQL, SongRequest

class SongApiMapper:

    def map_to_song_data_response(self, song_model: Song)->SongDataResponse:
        return SongDataResponse(id=song_model.id, title=song_model.title, artist=song_model.artist,
                                belongs_to_host_country=song_model.belongs_to_host_country,
                                jury_potential_score=song_model.jury_potential_score,
                                televote_potential_score=song_model.televote_potential_score, country=song_model.country.__dict__)

    def map_to_song_data_response_ql(self, song_model: Song)->SongDataResponseQL:
        return SongDataResponseQL(id=song_model.id, title=song_model.title, artist=song_model.artist,
                                  belongs_to_host_country=song_model.belongs_to_host_country,
                                  jury_potential_score=ScoreEnum(song_model.jury_potential_score).value,
                                  televote_potential_score=ScoreEnum(song_model.televote_potential_score).value, 
                                  country=CountryApiMapper().map_to_country_without_songs_votings_data_response_ql(song_model.country)) 
    
    def map_to_song_model(self, song_schema: SongRequest)->Song:
        Song.model_rebuild()
        return Song(title=song_schema.title, artist=song_schema.artist,
                    belongs_to_host_country=song_schema.belongs_to_host_country,
                    jury_potential_score=song_schema.jury_potential_score,
                    televote_potential_score=song_schema.televote_potential_score,
                    event=Event(id=song_schema.event_id), country=Country(id=song_schema.country_id))