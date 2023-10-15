from app.logic.models import Ceremony, CeremonyType, Country, Event, Song
from app.persistence.entities import CeremonyEntity, CeremonyTypeEntity, CountryEntity, EventEntity, SongEntity

class CeremonyModelMapper:

    def map_to_ceremony_entity(self, ceremony: Ceremony)->CeremonyEntity:
        return CeremonyEntity(id=ceremony.id, ceremony_type_id=ceremony.ceremony_type.id, 
                            event_id=ceremony.event.id, date=ceremony.date)
    
    def map_to_ceremony_model_without_event(self, ceremony_entity: CeremonyEntity)->Ceremony:
        if ceremony_entity is None:
            return None
        ceremony_type = CeremonyModelMapper().map_to_ceremony_type_model(ceremony_entity.ceremony_type)
        return Ceremony(id=ceremony_entity.id, date=ceremony_entity.date, ceremony_type=ceremony_type, 
                        songs=ceremony_entity.songs, votings=ceremony_entity.votings)

    def map_to_ceremony_type_model(self, ceremony_type_entity: CeremonyTypeEntity)->CeremonyType:
        return CeremonyType(id=ceremony_type_entity.id, name=ceremony_type_entity.name, code=ceremony_type_entity.code)
    


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
    

    def map_to_song_model_without_submodels(self, song_entity: SongEntity)->Song:
        if song_entity is None:
            return None
        
        return Song(id=song_entity.id, title=song_entity.title, artist=song_entity.artist, 
                    jury_potential_score=song_entity.jury_potential_score, 
                    televote_potential_score=song_entity.televote_potential_score,
                    belongs_to_host_country=song_entity.belongs_to_host_country)

    def map_to_song_model(self, song_entity: SongEntity)->Song:
        event = EventModelMapper().map_to_event_model_without_submodels(event_entity=song_entity.event)
        country = CountryModelMapper().map_to_country_model_without_submodels(country_entity=song_entity.country)
        Song.model_rebuild()
        song = self.map_to_song_model_without_submodels(song_entity=song_entity)
        if song is not None:
            song.country = country
            song.event = event

        return song

class CountryModelMapper:

    def map_to_country_entity(self, country: Country)->CountryEntity:
        return CountryEntity(id=country.id, name=country.name, code=country.code)
    

    def map_to_country_model_without_submodels(self, country_entity: CountryEntity)->Country:
        if country_entity is None:
            return None
        return Country(id=country_entity.id, name=country_entity.name, code=country_entity.code)


    def map_to_country_model(self, country_entity: CountryEntity)->Country:
        songs = [SongModelMapper().map_to_song_model_without_submodels(song) for song in country_entity.songs]
        country = self.map_to_country_model_without_submodels(country_entity=country_entity)
        if country is not None:
            country.songs = songs

        return country


class EventModelMapper:

    def map_to_event_entity(self, event: Event)->EventEntity:
        return EventEntity(id=event.id, year=event.year, slogan=event.slogan, host_city=event.host_city, arena=event.arena) 


    def map_to_event_model_without_submodels(self, event_entity: EventEntity)->Event:
        if event_entity is None:
            return None
        return Event(id=event_entity.id, year=event_entity.year, slogan=event_entity.slogan, 
                    host_city=event_entity.host_city, arena=event_entity.arena)
    
    
    def map_to_event_model(self, event_entity: EventEntity)->Event:
        ceremonies = [CeremonyModelMapper().map_to_ceremony_model_without_event(ceremony) for ceremony in event_entity.ceremonies]
        event = self.map_to_event_model_without_submodels(event_entity=event_entity)
        if event is not None:
            event.ceremonies = ceremonies

        return event



