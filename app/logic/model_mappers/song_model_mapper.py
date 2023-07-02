from app.logic.models import Song
from app.persistence.entities import SongEntity
from app.logic.model_mappers import event_model_mapper, country_model_mapper

def map_to_song_entity(song: Song)->SongEntity:
    country_entity = country_model_mapper.map_to_country_entity(song.country)
    event_entity = event_model_mapper.map_to_event_entity(song.event)
    return SongEntity(id=song.id, title=song.title, artist=song.artist, 
                        jury_potential_score=song.jury_potential_score, 
                        televote_potential_score=song.televote_potential_score,
                        belongs_to_host_country=song.belongs_to_host_country,
                        country=country_entity, event=event_entity,
                        country_id=country_entity.id, event_id=event_entity.id)


def map_to_song_model(song_entity: SongEntity)->Song:
    event = event_model_mapper.map_to_event_model(song_entity.event)
    country = country_model_mapper.map_to_country_model(song_entity.country)
    return Song(id=song_entity.id, title=song_entity.title, artist=song_entity.artist, 
                jury_potential_score=song_entity.jury_potential_score, 
                televote_potential_score=song_entity.televote_potential_score,
                belongs_to_host_country=song_entity.belongs_to_host_country,
                country=country, event=event)