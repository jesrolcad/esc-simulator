from sqlalchemy import select, insert
from app.persistence.entities import SongEntity
from app.persistence.repositories.base_repository import BaseRepository

class SongRepository(BaseRepository):

    def get_song(self, song_id: int)-> SongEntity:
        return self.session.scalars(select(SongEntity).where(SongEntity.id == song_id)).first()


    def get_songs(self)-> SongEntity:
        return self.session.scalars(select(SongEntity)).all()
    


    def create_song(self, song: SongEntity)-> SongEntity:
        insert_stmt = (insert(SongEntity).values(title=song.title, artist=song.artist, 
                        jury_potential_score=song.jury_potential_score, 
                        televote_potential_score=song.televote_potential_score,
                        belongs_to_host_country=song.belongs_to_host_country,
                        country_id=song.country_id, event_id=song.event_id).returning(SongEntity.id))
        
        result = self.session.execute(insert_stmt.returning(SongEntity.id))
        country_id = result.fetchone()[0]

        song.id = country_id
        return song

