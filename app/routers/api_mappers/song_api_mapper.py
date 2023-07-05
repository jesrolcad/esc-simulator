from app.logic.models import Song
from app.routers.schemas.song_schemas import SongDataResponse

def map_to_song_data_response(song_model: Song)->SongDataResponse:
    return SongDataResponse(id=song_model.id, title=song_model.title, artist=song_model.artist,
                            belongs_to_host_country=song_model.belongs_to_host_country,
                            jury_potential_score=song_model.jury_potential_score,
                            televote_potential_score=song_model.televote_potential_score,
                            event=song_model.event, country=song_model.country,
                            ceremonies=song_model.ceremonies, votings=song_model.votings)