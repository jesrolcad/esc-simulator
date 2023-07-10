from random import randint
from app.logic.models import Song
from app.persistence.repositories.song_repository import SongRepository
from app.persistence.repositories.country_repository import CountryRepository
from app.persistence.repositories.event_repository import EventRepository
from app.logic.services.base_service import BaseService
from app.logic.model_mappers.song_model_mapper import SongModelMapper
from app.utils.exceptions import NotFoundError, AlreadyExistsError, BusinessLogicValidationError

class SongService(BaseService):

    def get_song(self, song_id: int)-> Song:
        song = SongRepository(self.session).get_song(song_id)
        if song is None:
            raise NotFoundError(f"Song with id {song_id} not found")
        
        return SongModelMapper().map_to_song_model(song_entity=song)
    
    def get_songs(self, title: str, country_code: str, event_year: int)-> list:
        return [SongModelMapper().map_to_song_model(song_entity=song) for song in SongRepository(self.session)
                .get_songs(title=title, country_code=country_code, event_year=event_year)]

    def create_song(self, song: Song)-> Song:
        song_entity = SongModelMapper().map_to_song_entity(song=song)
        self.check_associated_country_and_event_exist(country_id=song_entity.country_id, event_id=song_entity.event_id)
        existing_song_by_country_and_event = SongRepository(self.session).get_song_by_country_and_event_id(country_id=song_entity.country_id,
                                                                                                            event_id=song_entity.event_id)
        if existing_song_by_country_and_event:
            raise AlreadyExistsError(message=f"Song for country_id {song_entity.country_id} and event_id {song_entity.event_id} already exists")

        if song_entity.belongs_to_host_country:
            self.check_if_another_song_marked_as_belongs_to_host_country(event_id=song_entity.event_id)

        
        
        return SongModelMapper().map_to_song_model(SongRepository(self.session).create_song(song=song_entity))
    
    def check_associated_country_and_event_exist(self, country_id: int, event_id: int):
        country = CountryRepository(self.session).get_country(id=country_id)
        event = EventRepository(self.session).get_event(id=event_id)
        if country is None and event is None:
            raise BusinessLogicValidationError(field="country_id, event_id",message=f"Country with id {country_id} and event with id {event_id} not found")
        if country is None:
            raise BusinessLogicValidationError(field="country_id",message=f"Country with id {country_id} not found")
        if event is None:
            raise BusinessLogicValidationError(field="event_id",message=f"Event with id {event_id} not found")
        
    
    def check_if_another_song_marked_as_belongs_to_host_country(self, event_id: int):
        song_id = SongRepository(self.session).check_existing_song_marked_as_belongs_to_host_country(event_id=event_id)
        if song_id:
            raise BusinessLogicValidationError(f"Song with id {song_id} is already marked as belongs to host country.")

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