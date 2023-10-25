from app.logic.models import Event
from app.routers.schemas.event_schemas import EventDataResponse
from .ceremony_api_mapper import CeremonyApiMapper

class EventApiMapper:

    def map_to_event_data_response(self, event_model: Event)->EventDataResponse:
        ceremonies = [CeremonyApiMapper().map_to_ceremony_without_event_data_response(ceremony) for ceremony in event_model.ceremonies]
        return EventDataResponse(id=event_model.id, year=event_model.year, slogan=event_model.slogan, host_city=event_model.host_city, arena=event_model.arena, ceremonies=ceremonies)
