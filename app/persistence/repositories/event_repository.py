from sqlalchemy import select, insert, or_
from app.persistence.entities import EventEntity
from app.db.database import get_db

def get_event(id: int, year: int)->EventEntity:
    with get_db() as db_session:
        query = select(EventEntity)
        if id is not None and year is not None:
            query = query.where(or_(EventEntity.id == id, EventEntity.year == year))
        elif id is not None:
            query = query.where(EventEntity.id == id)
        elif year is not None:
            query = query.where(EventEntity.year == year)
        return db_session.scalars(query).first()

def create_event(event: EventEntity)->EventEntity:
    with get_db() as db_session:
        insert_stmt = (insert(EventEntity).values(year=event.year, slogan=event.slogan, 
                        host_city=event.host_city, arena=event.arena).returning(EventEntity.id))
        
        result = db_session.execute(insert_stmt.returning(EventEntity.id))
        event_id = result.fetchone()[0]

        event.id = event_id
        return event

