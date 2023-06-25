from app.persistence.repositories import event_repository
from app.logic.model_mappers import event_model_mapper
from app.logic.models.event import Event

def get_event(id: int = None, year: int = None)->Event:
    event_entity = event_repository.get_event(id, year)
    return event_model_mapper.map_to_event_model(event_entity)


def create_event(event: Event)->int:
    event_entity = event_model_mapper.map_to_event_entity(event)
    # Create associated ceremonies
    
    return event_repository.create_event(event_entity)