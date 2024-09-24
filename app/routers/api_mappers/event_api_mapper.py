from app.logic.models import Event
from app.routers.schemas.base_schemas import BaseEventQL
from app.routers.schemas.event_schemas import EventDataResponse
from app.routers.schemas.event_schemas import EventRequest
from .ceremony_api_mapper import CeremonyApiMapper


class EventApiMapper:

    def map_to_event_data_response(self, event_model: Event)->EventDataResponse:
        ceremonies = [CeremonyApiMapper().map_to_ceremony_without_event_data_response(ceremony) for ceremony in event_model.ceremonies]
        return EventDataResponse(id=event_model.id, year=event_model.year, slogan=event_model.slogan, host_city=event_model.host_city, 
                                 arena=event_model.arena, ceremonies=ceremonies)
    

    def map_to_event_model(self, event_schema: EventRequest)->Event:
        return Event(year=event_schema.year, slogan=event_schema.slogan, host_city=event_schema.host_city, arena=event_schema.arena)
    
    def map_event_request_ql_to_event_model(self, event_schema_ql: BaseEventQL)->Event:
        return Event(year=event_schema_ql.year, slogan=event_schema_ql.slogan, host_city=event_schema_ql.host_city, arena=event_schema_ql.arena)
