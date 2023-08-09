from app.logic.models import Song, Event, Country
from app.routers.schemas.song_schemas import SongDataResponse, SongRequest

class SongApiMapper:

    def map_to_song_data_response(self, song_model: Song)->SongDataResponse:
        return SongDataResponse(id=song_model.id, title=song_model.title, artist=song_model.artist,
                                belongs_to_host_country=song_model.belongs_to_host_country,
                                jury_potential_score=song_model.jury_potential_score,
                                televote_potential_score=song_model.televote_potential_score,
                                event=song_model.event.__dict__, country=song_model.country.__dict__,
                                ceremonies=song_model.ceremonies, votings=song_model.votings) 
    
    def map_to_song_model(self, song_schema: SongRequest)->Song:
        Song.model_rebuild()
        return Song(title=song_schema.title, artist=song_schema.artist,
                    belongs_to_host_country=song_schema.belongs_to_host_country,
                    jury_potential_score=song_schema.jury_potential_score,
                    televote_potential_score=song_schema.televote_potential_score,
                    event=Event(id=song_schema.event_id), country=Country(id=song_schema.country_id))