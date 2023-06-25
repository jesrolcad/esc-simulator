from datetime import datetime, timedelta
from app.persistence.repositories import event_repository, ceremony_repository
from app.logic.model_mappers import event_model_mapper, ceremony_model_mapper
from app.logic.models.event import Event
from app.logic.models.ceremony import Ceremony

def get_event(id: int = None, year: int = None)->Event:
    event_entity = event_repository.get_event(id, year)
    return event_model_mapper.map_to_event_model(event_entity)


def create_event_and_associated_ceremonies(event: Event, grand_final_date: datetime)->int:
    event_entity = event_model_mapper.map_to_event_entity(event)
    event_id = event_repository.create_event(event_entity)
    associate_ceremonies_to_event(event, grand_final_date)

    return event_id


def associate_ceremonies_to_event(event: Event, grand_final_date: datetime):
    semifinal1_date = grand_final_date - timedelta(days=4)
    semifinal2_date = grand_final_date - timedelta(days=2)

    first_semifinal_ceremony_type = ceremony_repository.get_ceremony_type(code='SF1')
    second_semifinal_ceremony_type = ceremony_repository.get_ceremony_type(code='SF2')
    grand_final_ceremony_type = ceremony_repository.get_ceremony_type(code='GF')

    first_semifinal_ceremony = Ceremony(date=semifinal1_date, ceremony_type=first_semifinal_ceremony_type, event=event)
    second_semifinal_ceremony = Ceremony(date=semifinal2_date, ceremony_type=second_semifinal_ceremony_type, event=event)
    grand_final_ceremmony = Ceremony(date=grand_final_date, ceremony_type=grand_final_ceremony_type, event=event)

    ceremony_repository.create_ceremony(ceremony_model_mapper.map_to_ceremony_entity(first_semifinal_ceremony))
    ceremony_repository.create_ceremony(ceremony_model_mapper.map_to_ceremony_entity(second_semifinal_ceremony))
    ceremony_repository.create_ceremony(ceremony_model_mapper.map_to_ceremony_entity(grand_final_ceremmony))

