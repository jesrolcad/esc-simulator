from app.persistence.entities import EventEntity
from app.logic.models import Event

def map_to_event_entity(event: Event)->EventEntity:
    return EventEntity(year=event.year, slogan=event.slogan, host_city=event.host_city, arena=event.arena) 


def map_to_event_model(event_entity: EventEntity)->Event:
    if event_entity is None:
        return None
    print(f"Event entity id: {event_entity.id}")
    return Event(id=event_entity.id, year=event_entity.year, slogan=event_entity.slogan, host_city=event_entity.host_city, arena=event_entity.arena)