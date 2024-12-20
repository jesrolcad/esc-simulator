from operator import is_
from random import randint
from app.logic.models import SimulationSong, Song
from app.persistence.repositories.song_repository import SongRepository
from app.persistence.repositories.event_repository import EventRepository
from app.persistence.repositories.country_repository import CountryRepository
from app.logic.services.country_service import CountryService
from app.persistence.entities import SongEntity
from app.logic.services.base_service import BaseService
from app.logic.model_mappers import SongModelMapper
from app.utils.exceptions import NotFoundError, AlreadyExistsError, BusinessLogicValidationError

class SongService(BaseService):

    def get_song(self, song_id: int)-> Song:
        song = SongRepository(self.session).get_song(song_id)
        if song is None:
            raise NotFoundError(field="song_id",message=f"Song with id {song_id} not found")
        
        return SongModelMapper().map_to_song_model(song_entity=song)
    
    def get_songs(self, title: str, country_code: str, event_year: int)-> list:
        return [SongModelMapper().map_to_song_model(song_entity=song) for song in SongRepository(self.session)
                .get_songs(title=title, country_code=country_code, event_year=event_year)]
    

    def get_song_summary(self, song_id: int, title: str, artist: str, country_name: str)->str:
        if country_name is None:
            country = CountryService(self.session).get_country_by_song_id(song_id=song_id)
            country_name = country.name

        return f"{country_name}. {artist} - {title}"

    def get_songs_by_country_id(self, country_id: int)->list[Song]:
        songs = SongRepository(self.session).get_songs_by_country_id(country_id=country_id)

        return [SongModelMapper().map_to_song_model_without_submodels(song_entity=song_entity) for song_entity in songs]

    
    def get_simulation_songs_by_event_id(self, event_id: int)->list[SimulationSong]:
        simulation_songs = SongRepository(self.session).get_simulation_songs_info_by_event_id(event_id=event_id)

        return SongModelMapper().map_to_simulation_song_model_list(rows=simulation_songs)
    
    def get_simulation_songs_by_ceremony_id(self, ceremony_id: int)->list[SimulationSong]:
        simulation_songs = SongRepository(self.session).get_simulation_songs_info_by_ceremony_id(ceremony_id=ceremony_id)

        return SongModelMapper().map_to_simulation_song_model_list(rows=simulation_songs)

    def get_automatic_qualified_songs_for_grand_final_by_event_id(self, event_id: int)->SongModelMapper.CountrySong:
        country_song_ids = SongRepository(self.session).get_automatic_qualified_songs_for_grand_final_by_event_id(event_id=event_id)

        return SongModelMapper().map_to_song_country_ids(rows=country_song_ids)

    def create_song(self, song: Song)-> Song:
        song_entity = SongModelMapper().map_to_song_entity(song=song)
        self.validate_song(song_entity=song_entity)

        return SongModelMapper().map_to_song_model_without_submodels(SongRepository(self.session).create_song(song=song_entity))

    def update_song(self, song_id: int, updated_song: Song):
        self.get_song(song_id=song_id)
        is_participating_in_ceremony = self.check_song_is_participating_in_a_ceremony(song_id=song_id)

        if is_participating_in_ceremony:
            raise BusinessLogicValidationError(field="song_id",message=f"Song with id {song_id} cannot be updated because it is participating in a ceremony")
        
        updated_song_entity = SongModelMapper().map_to_song_entity(song=updated_song)
        updated_song_entity.id = song_id
        self.validate_song(song_entity=updated_song_entity)

        SongRepository(self.session).update_song(song=updated_song_entity)
    
    def delete_song(self, song_id: int):
        self.get_song(song_id=song_id)
        is_participating_in_ceremony = self.check_song_is_participating_in_a_ceremony(song_id=song_id)
        
        if is_participating_in_ceremony:
            raise BusinessLogicValidationError(field="song_id",message=f"Song with id {song_id} cannot be deleted because it is participating in a ceremony")
        SongRepository(self.session).delete_song(song_id=song_id)


    def validate_song(self, song_entity: SongEntity):
        self.check_associated_country_and_event_exist(country_id=song_entity.country_id, event_id=song_entity.event_id)
        existing_song_by_country_and_event = SongRepository(self.session).get_song_by_country_and_event_id(song_id=song_entity.id,country_id=song_entity.country_id,
                                                                                                            event_id=song_entity.event_id)
        if existing_song_by_country_and_event:
            raise AlreadyExistsError(field="country_id, event_id",message=f"Song for country_id {song_entity.country_id} and event_id {song_entity.event_id} already exists")

        if song_entity.belongs_to_host_country:
            self.check_if_another_song_marked_as_belongs_to_host_country(song_id=song_entity.id,event_id=song_entity.event_id)


    def check_associated_country_and_event_exist(self, country_id: int, event_id: int):
        country = CountryRepository(self.session).get_country(id=country_id)
        event = EventRepository(self.session).get_event(id=event_id)
        if country is None and event is None:
            raise BusinessLogicValidationError(field="country_id, event_id",message=f"Country with id {country_id} and event with id {event_id} not found")
        if country is None:
            raise BusinessLogicValidationError(field="country_id",message=f"Country with id {country_id} not found")
        if event is None:
            raise BusinessLogicValidationError(field="event_id",message=f"Event with id {event_id} not found")
        
    
    def check_if_another_song_marked_as_belongs_to_host_country(self, song_id: int, event_id: int):
        retrieved_song_id = SongRepository(self.session).check_existing_song_marked_as_belongs_to_host_country(song_id=song_id, event_id=event_id)
        if retrieved_song_id:
            raise BusinessLogicValidationError(field="belongs_to_host_country",message=f"Song with id {retrieved_song_id} is already marked as belongs to host country.")

    def check_song_is_participating_in_a_ceremony(self, song_id: int)->bool:
        return SongRepository(self.session).check_is_song_participating_in_a_ceremony(song_id=song_id)

    def calculate_potential_scores(self, position: int)-> tuple: 
        """
        Calculate the potential scores for a song based on its position in the final ranking
        returns a tuple: (jury_potential_score, televote_potential_score) 
        """

        jury_potential_score, televote_potential_score = 0, 0

        if position in range(1,4):
            jury_potential_score, televote_potential_score = (randint(9, 10), randint(9, 10))
        
        elif position in range (4, 6):
            jury_potential_score, televote_potential_score = (randint(8, 9), randint(8, 9))
        
        elif position in range (6, 11):
            jury_potential_score, televote_potential_score = (randint(7, 9), randint(7, 9))
        
        elif position in range (11, 16):
            jury_potential_score, televote_potential_score = (randint(6, 8), randint(6, 8))
        
        elif position in range (16, 21):
            jury_potential_score, televote_potential_score = (randint(5, 7), randint(5, 7))
        
        elif position in range (21, 28):
            jury_potential_score, televote_potential_score = (randint(2, 5), randint(2, 5))

        else:
            jury_potential_score, televote_potential_score = (randint(1, 4), randint(1, 4))

        return (jury_potential_score, televote_potential_score)