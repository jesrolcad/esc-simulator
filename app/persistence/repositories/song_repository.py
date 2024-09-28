from typing import Any
from sqlalchemy import exists, select, insert, and_, or_, update, delete, Sequence
from app.persistence.entities import SongEntity, CountryEntity, EventEntity, SongCeremony
from app.persistence.repositories.base_repository import BaseRepository
from app.utils.constants import BIG_FIVE_IDS


class SongRepository(BaseRepository):

    def get_songs(self, title: str, country_code: str, event_year: int)-> SongEntity:
        
        return self.session.scalars(select(SongEntity).join(CountryEntity).join(EventEntity).filter(and_(
            or_(SongEntity.title.ilike(f"%{title}%"), title is None),
            or_(CountryEntity.code == country_code, country_code is None),
            or_(EventEntity.year == event_year, event_year is None)
        ))).all()

    def get_song(self, song_id: int)-> SongEntity:
        return self.session.scalars(select(SongEntity).where(SongEntity.id == song_id)).first()
    
    def get_songs_by_country_id(self, country_id: int)-> list[SongEntity]:
        return self.session.scalars(select(SongEntity).where(SongEntity.country_id == country_id)).all()
    
    def get_simulation_songs_info_by_event_id(self, event_id: int)-> Sequence[Any]:
        return self.session.execute(select(SongEntity.id, SongEntity.country_id, SongEntity.jury_potential_score, SongEntity.televote_potential_score)
                                    .where(and_(SongEntity.event_id == event_id, 
                                                SongEntity.belongs_to_host_country.is_(False), 
                                                ~SongEntity.country_id.in_(BIG_FIVE_IDS)))).all()
    

    
    def get_simulation_songs_info_by_ceremony_id(self, ceremony_id: int)-> Sequence[Any]:
        return self.session.execute(select(SongEntity.id, SongEntity.country_id, SongEntity.jury_potential_score, SongEntity.televote_potential_score)
                                    .join(SongCeremony, SongEntity.id == SongCeremony.c.song_id).where(SongCeremony.c.ceremony_id == ceremony_id)).all()


    def get_song_by_country_and_event_id(self, song_id: int, country_id: int, event_id: int)-> SongEntity:
        return self.session.scalars(select(SongEntity).where(and_(SongEntity.id != song_id,SongEntity.country_id == country_id, 
                                                                SongEntity.event_id == event_id))).first()

    def get_automatic_qualified_songs_for_grand_final_by_event_id(self, event_id: int)-> Sequence[Any]:
        return self.session.execute(select(SongEntity.id, SongEntity.country_id).where(and_(SongEntity.event_id == event_id, 
                                                                or_(SongEntity.belongs_to_host_country.is_(True), 
                                                                SongEntity.country_id.in_(BIG_FIVE_IDS))))).all()
    

    def check_existing_song_marked_as_belongs_to_host_country(self, song_id: int, event_id: int)->int:
        return self.session.scalars(select(SongEntity.id).where(and_(bool(SongEntity.belongs_to_host_country), 
                                                                SongEntity.id != song_id, SongEntity.event_id == event_id))).first()

    def check_is_song_participating_in_a_ceremony(self, song_id: int)->bool:
        return self.session.scalars(select(exists().where(SongCeremony.c.song_id == song_id))).first()


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


    def update_song(self, song: SongEntity):
        update_stmt = (update(SongEntity).where(SongEntity.id == song.id)
                    .values(title=song.title, artist=song.artist,belongs_to_host_country=song.belongs_to_host_country,
                            jury_potential_score=song.jury_potential_score,televote_potential_score=song.televote_potential_score,
                            country_id=song.country_id, event_id=song.event_id))
        
        self.session.execute(update_stmt)

    def delete_song(self, song_id: int):
        delete_stmt = (delete(SongEntity).where(SongEntity.id == song_id))
        self.session.execute(delete_stmt)


    def delete_songs_from_ceremonies(self, ceremonies: list[int]):
        delete_stmt = (delete(SongCeremony).where(SongCeremony.c.ceremony_id.in_(ceremonies)))
        self.session.execute(delete_stmt)

    
    def delete_songs_by_event_id(self, event_id: int):
        delete_stmt = (delete(SongEntity).where(SongEntity.event_id == event_id))
        self.session.execute(delete_stmt)

