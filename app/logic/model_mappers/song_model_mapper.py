from app.logic.models import Song
from app.persistence.entities import SongEntity

def map_to_song_entity(song: Song)->SongEntity:
    return SongEntity(id=song.id, title=song.title, artist=song.artist, 
                        jury_potential_score=song.jury_potential_score, 
                        televote_potential_score=song.televote_potential_score,
                        belongs_to_host_country=song.belongs_to_host_country,
                        country_id=song.country.id, event_id=song.event.id)


def map_to_song_model(song_entity: SongEntity)->Song:
    return Song(id=song_entity.id, title=song_entity.title, artist=song_entity.artist, 
                jury_potential_score=song_entity.jury_potential_score, 
                televote_potential_score=song_entity.televote_potential_score,
                belongs_to_host_country=song_entity.belongs_to_host_country,
                country_id=song_entity.country_id, event_id=song_entity.event_id)