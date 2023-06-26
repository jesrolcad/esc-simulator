from sqlalchemy import insert
from app.persistence.entities import SongEntity
from app.db.database import get_db


def create_song(song: SongEntity)-> SongEntity:
    with get_db() as db_session:
        insert_stmt = (insert(SongEntity).values(title=song.title, artist=song.artist, 
                        jury_potential_score=song.jury_potential_score, 
                        televote_potential_score=song.televote_potential_score,
                        belongs_to_host_country=song.belongs_to_host_country,
                        country_id=song.country_id, event_id=song.event_id).returning(SongEntity.id))
        
        result = db_session.execute(insert_stmt.returning(SongEntity.id))
        country_id = result.fetchone()[0]

        song.id = country_id
        return song

