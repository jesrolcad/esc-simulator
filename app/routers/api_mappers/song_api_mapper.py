from app.logic.models import Song, Event, Country
from app.routers.schemas.song_schemas import SongDataResponse, SongRequest, SongRequestQL
from app.routers.schemas.common_schemas import SongWithoutCountryCeremoniesVotingsQL

class SongApiMapper:

    def map_to_song_data_response(self, song_model: Song)->SongDataResponse:
        return SongDataResponse(id=song_model.id, title=song_model.title, artist=song_model.artist,
                                belongs_to_host_country=song_model.belongs_to_host_country,
                                jury_potential_score=song_model.jury_potential_score,
                                televote_potential_score=song_model.televote_potential_score, country=song_model.country.__dict__)
 
    
    def map_to_song_model(self, song_schema: SongRequest)->Song:
        Song.model_rebuild()
        return Song(title=song_schema.title, artist=song_schema.artist,
                    belongs_to_host_country=song_schema.belongs_to_host_country,
                    jury_potential_score=song_schema.jury_potential_score,
                    televote_potential_score=song_schema.televote_potential_score,
                    event=Event(id=song_schema.event_id), country=Country(id=song_schema.country_id))
    
    def map_song_request_ql_to_song_model(self, song_schema_ql: SongRequestQL)->Song:
        Song.model_rebuild()
        return Song(title=song_schema_ql.title, artist=song_schema_ql.artist,
                    belongs_to_host_country=song_schema_ql.belongs_to_host_country,
                    jury_potential_score=song_schema_ql.jury_potential_score.value,
                    televote_potential_score=song_schema_ql.televote_potential_score.value,
                    event=Event(id=song_schema_ql.event_id), country=Country(id=song_schema_ql.country_id))
    
    def map_to_song_without_country_ceremonies_votings_ql(self, song_model: Song)->SongWithoutCountryCeremoniesVotingsQL:
        return SongWithoutCountryCeremoniesVotingsQL(id=song_model.id, title=song_model.title, artist=song_model.artist,
                                                    belongs_to_host_country=song_model.belongs_to_host_country,
                                                    jury_potential_score=song_model.jury_potential_score,
                                                    televote_potential_score=song_model.televote_potential_score)