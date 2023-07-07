from app.persistence.entities import EventEntity
from app.logic.models import Event


class EventModelMapper:

    def map_to_event_entity(self, event: Event)->EventEntity:
        return EventEntity(id=event.id, year=event.year, slogan=event.slogan, host_city=event.host_city, arena=event.arena) 


    def map_to_event_model(self, event_entity: EventEntity)->Event:
        if event_entity is None:
            return None
        return Event(id=event_entity.id, year=event_entity.year, slogan=event_entity.slogan, host_city=event_entity.host_city, arena=event_entity.arena)