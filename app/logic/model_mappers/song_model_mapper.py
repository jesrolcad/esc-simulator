from app.logic.models import Song
from app.persistence.entities import SongEntity
from app.logic.model_mappers.event_model_mapper import EventModelMapper
from app.logic.model_mappers.country_model_mapper import CountryModelMapper

class SongModelMapper:

    def map_to_song_entity(self, song: Song)->SongEntity:
        
        country_entity = CountryModelMapper().map_to_country_entity(song.country)
        event_entity = EventModelMapper().map_to_event_entity(song.event)
        return SongEntity(id=song.id, title=song.title, artist=song.artist, 
                            jury_potential_score=song.jury_potential_score, 
                            televote_potential_score=song.televote_potential_score,
                            belongs_to_host_country=song.belongs_to_host_country,
                            country=country_entity, event=event_entity,
                            country_id=country_entity.id, event_id=event_entity.id)


    def map_to_song_model(self, song_entity: SongEntity)->Song:
        if song_entity is None:
            return None
        
        event = EventModelMapper().map_to_event_model(event_entity=song_entity.event)
        country = CountryModelMapper().map_to_country_model(country_entity=song_entity.country)
        Song.update_forward_refs()
        return Song(id=song_entity.id, title=song_entity.title, artist=song_entity.artist, 
                    jury_potential_score=song_entity.jury_potential_score, 
                    televote_potential_score=song_entity.televote_potential_score,
                    belongs_to_host_country=song_entity.belongs_to_host_country,
                    country=country, event=event)