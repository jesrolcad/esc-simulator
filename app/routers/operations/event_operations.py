import strawberry

from app.logic.services.ceremony_service import CeremonyService
from app.logic.services.event_service import EventService
from app.routers.api_mappers.ceremony_api_mapper import CeremonyApiMapper
from app.routers.api_mappers.event_api_mapper import EventApiMapper
from app.routers.schemas.api_schemas import ResultResponseQL
from app.routers.schemas.base_schemas import BaseEventQL, BaseIdQL
from app.routers.schemas.common_schemas import CeremonyWithoutEventDataResponseQL
from app.routers.schemas.event_schemas import CreateEventRequestQL, UpdateEventRequestQL
from app.routers.operations.validators import validate_event_request_ql, validate_create_event_request_ql

@strawberry.type
class EventDataResponseQL(BaseEventQL, BaseIdQL):
    
    @strawberry.field
    def ceremonies(self, info: strawberry.Info)->list[CeremonyWithoutEventDataResponseQL]:
        ceremonies = CeremonyService(info.context.db).get_ceremonies_with_ceremony_types_by_event_id(event_id=self.id)
        return [CeremonyApiMapper().map_to_ceremony_without_event_data_response_ql(ceremony) for ceremony in ceremonies]

    @staticmethod 
    def map_to_event_data_response_ql(event)->'EventDataResponseQL':
        return EventDataResponseQL(id=event.id, year=event.year, slogan=event.slogan, host_city=event.host_city, arena=event.arena)

@strawberry.type
class EventQuery:
    @strawberry.field
    def events(self, info: strawberry.Info)->list[EventDataResponseQL]:
        response = EventService(info.context.db).get_events(submodels=False)
        return [EventDataResponseQL.map_to_event_data_response_ql(event) for event in response]
    
    @strawberry.field
    def event(self, info: strawberry.Info, event_id: int)->EventDataResponseQL:
        response = EventService(info.context.db).get_event(id=event_id, submodels=False)
        return EventDataResponseQL.map_to_event_data_response_ql(response)
    
@strawberry.type
class EventMutation:
    @strawberry.mutation
    def create_event(self, info: strawberry.Info, event: CreateEventRequestQL)->EventDataResponseQL:
        validate_create_event_request_ql(event=event)
        event_model = EventApiMapper().map_event_request_ql_to_event_model(event_schema_ql=event)
        event = EventService(info.context.db).create_event_and_associated_ceremonies(event=event_model, grand_final_date=event.grand_final_date)
        return EventDataResponseQL.map_to_event_data_response_ql(event)
    
    @strawberry.mutation
    def update_event(self, info: strawberry.Info, event_id: int, event: UpdateEventRequestQL)->ResultResponseQL:
        validate_event_request_ql(event=event)
        event_model = EventApiMapper().map_event_request_ql_to_event_model(event_schema_ql=event)
        EventService(info.context.db).update_event(event_id=event_id, event=event_model)
        return ResultResponseQL(success=True, message=f"Event with id {event_id} updated successfully")
    
    @strawberry.mutation
    def delete_event(self, info: strawberry.Info, event_id: int)->ResultResponseQL:
        EventService(info.context.db).delete_event(event_id=event_id)
        return ResultResponseQL(success=True, message=f"Event with id {event_id} deleted successfully")
