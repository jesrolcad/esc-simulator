from sqlalchemy import select, insert, and_, or_, update
from app.persistence.entities import SongEntity, CountryEntity, EventEntity
from app.persistence.repositories.base_repository import BaseRepository

class SongRepository(BaseRepository):

    def get_songs(self, title: str, country_code: str, event_year: int)-> SongEntity:
        
        return self.session.scalars(select(SongEntity).join(CountryEntity).join(EventEntity).filter(and_(
            or_(SongEntity.title.ilike(f"%{title}%"), title is None),
            or_(CountryEntity.code == country_code, country_code is None),
            or_(EventEntity.year == event_year, event_year is None)
        ))).all()

    def get_song(self, song_id: int)-> SongEntity:
        return self.session.scalars(select(SongEntity).where(SongEntity.id == song_id)).first()


    def get_song_by_country_and_event_id(self, country_id: int, event_id: int)-> SongEntity:
        return self.session.scalars(select(SongEntity).where(and_(SongEntity.country_id == country_id, SongEntity.event_id == event_id))).first()
    

    def check_existing_song_marked_as_belongs_to_host_country(self, event_id)->int:
        return self.session.scalars(select(SongEntity.id).where(and_(bool(SongEntity.belongs_to_host_country), SongEntity.event_id == event_id))).first()


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


    def update_song(self, song: SongEntity)-> SongEntity:
        update_stmt = (update(SongEntity).where(SongEntity.id == song.id)
                    .values(title=song.title, artist=song.artist,belongs_to_host_country=song.belongs_to_host_country,
                            jury_potential_score=song.jury_potential_score,televote_potential_score=song.televote_potential_score,
                            country_id=song.country_id, event_id=song.event_id))
        
        result = self.session.execute(update_stmt.returning(SongEntity.id))
        song_id = result.fetchone()[0]

        song.id = song_id
        return song

