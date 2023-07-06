from random import randint
from app.logic.models import Song
from app.persistence.repositories.song_repository import SongRepository
from app.logic.services.base_service import BaseService
from app.logic.model_mappers import song_model_mapper
from app.utils.exceptions import NotFoundError

class SongService(BaseService):

    def get_song(self, song_id: int)-> Song:
        song = SongRepository(self.session).get_song(song_id)
        if song is None:
            raise NotFoundError(f"Song with id {song_id} not found")
        
        return song_model_mapper.map_to_song_model(song)

    def create_song(self, song: Song)-> Song:
        song_entity = song_model_mapper.map_to_song_entity(song)
        return song_model_mapper.map_to_song_model(SongRepository(self.session).create_song(song_entity))

    def get_songs(self, title: str, country_code: str, event_year: int)-> list:
        return [song_model_mapper.map_to_song_model(song) for song in SongRepository(self.session).get_songs(title=title, country_code=country_code, event_year=event_year)]

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