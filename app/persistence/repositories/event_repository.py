from sqlalchemy import select, insert, update
from app.persistence.entities import EventEntity
from app.persistence.repositories.base_repository import BaseRepository

class EventRepository(BaseRepository):

    def get_events(self)->list[EventEntity]:
        query = select(EventEntity)
        return self.session.scalars(query).all()

    def get_event(self, id: int = None, year: int = None)->EventEntity:
        if id is None and year is None:
            raise ValueError("Id or year must be provided")

        query = select(EventEntity)
        if id is not None:
            query = query.where(EventEntity.id == id)
        elif year is not None:
            query = query.where(EventEntity.year == year)

        return self.session.scalars(query).first()

    def create_event(self, event: EventEntity)->EventEntity:
        insert_stmt = (insert(EventEntity).values(year=event.year, slogan=event.slogan, 
                        host_city=event.host_city, arena=event.arena).returning(EventEntity.id))
        
        result = self.session.execute(insert_stmt.returning(EventEntity.id))
        event_id = result.fetchone()[0]

        event.id = event_id

        return event

    def update_event(self, event: EventEntity):
        update_stmt = (update(EventEntity).where(EventEntity.id == event.id)
                        .values(year=event.year, slogan=event.slogan, host_city=event.host_city, arena=event.arena))

        self.session.execute(update_stmt)


