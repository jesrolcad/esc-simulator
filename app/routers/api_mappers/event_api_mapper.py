from app.logic.models import Event
from app.routers.schemas.base_schemas import BaseEvent, BaseEventQL
from app.routers.schemas.event_schemas import CreateEventRequest, CreateEventRequestQL, EventDataResponse, UpdateEventRequest
from .ceremony_api_mapper import CeremonyApiMapper


class EventApiMapper:

    def map_to_event_data_response(self, event_model: Event)->EventDataResponse:
        ceremonies = [CeremonyApiMapper().map_to_ceremony_without_event_data_response(ceremony) for ceremony in event_model.ceremonies]
        return EventDataResponse(id=event_model.id, year=event_model.year, slogan=event_model.slogan, host_city=event_model.host_city, 
                                 arena=event_model.arena, ceremonies=ceremonies)
    

    def map_to_event_model(self, event_schema: BaseEvent)->Event:
        event_model = Event(slogan=event_schema.slogan, host_city=event_schema.host_city, arena=event_schema.arena)

        if isinstance(event_schema, CreateEventRequest):
            event_model.year = event_schema.year

        return event_model
    
    def map_event_request_ql_to_event_model(self, event_schema_ql: BaseEventQL)->Event:
        event_model = Event(slogan=event_schema_ql.slogan, host_city=event_schema_ql.host_city, arena=event_schema_ql.arena)

        if isinstance(event_schema_ql, CreateEventRequestQL):
            event_model.year = event_schema_ql.year

        return event_model
