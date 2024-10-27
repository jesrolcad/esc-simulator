from fastapi import APIRouter, Depends, status
from app.db.database import get_db 
from app.routers.endpoints.definitions.event_definitions import *
from app.logic.services.event_service import EventService
from app.logic.services.ceremony_service import CeremonyService
from app.routers.api_mappers.event_api_mapper import EventApiMapper, CeremonyApiMapper
from app.routers.schemas.event_schemas import CreateEventRequest, UpdateEventRequest
from app.routers.schemas.api_schemas import ResultResponse
from app.routers.schemas.common_schemas import BaseId

router = APIRouter(prefix="/events", tags=["events"])

@router.get(path="", summary=get_events_endpoint["summary"], description=get_events_endpoint["description"], 
            responses=get_events_endpoint["responses"])
async def get_events(db: get_db = Depends()):

    response = EventService(db).get_events()
    return [EventApiMapper().map_to_event_data_response(event) for event in response]


@router.get(path="/{event_id}", summary=get_event_endpoint["summary"], description=get_event_endpoint["description"],
            responses=get_event_endpoint["responses"])
async def get_event(event_id: int, db: get_db = Depends()):

    response = EventService(db).get_event(id=event_id)
    return EventApiMapper().map_to_event_data_response(response)

@router.get(path="/{event_id}/ceremonies/{ceremony_id}", summary=get_event_ceremony_endpoint["summary"], description=get_event_ceremony_endpoint["description"],
            responses=get_event_ceremony_endpoint["responses"])
async def get_event_ceremony(event_id: int, ceremony_id: int, db: get_db = Depends()):
    response = CeremonyService(db).get_event_ceremony(event_id=event_id, ceremony_id=ceremony_id)
    return CeremonyApiMapper().map_to_ceremony_without_event_data_response(ceremony=response)


@router.post(path="", summary=create_event_endpoint["summary"], description=create_event_endpoint["description"],
            responses=create_event_endpoint["responses"], status_code=status.HTTP_201_CREATED)
async def create_event(event: CreateEventRequest, db: get_db = Depends()):

    event_model = EventApiMapper().map_to_event_model(event_schema=event)
    event_response = EventService(db).create_event_and_associated_ceremonies(event=event_model, grand_final_date=event.grand_final_date)
    return ResultResponse(message="Event created successfully", data=BaseId(id=event_response.id))


@router.put(path="/{event_id}", summary=update_event_endpoint["summary"], description=update_event_endpoint["description"],
            responses=update_event_endpoint["responses"], status_code=status.HTTP_204_NO_CONTENT)
async def update_event(event_id: int, event: UpdateEventRequest, db: get_db = Depends()):
    
    event_model = EventApiMapper().map_to_event_model(event_schema=event)
    EventService(db).update_event(event_id=event_id,event=event_model)
    return ResultResponse(message="Event updated successfully")

@router.delete(path="/{event_id}", summary=delete_event_endpoint["summary"], description=delete_event_endpoint["description"],
               responses=delete_event_endpoint["responses"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: get_db = Depends()):
    EventService(db).delete_event(event_id=event_id)

    return ResultResponse(message="Event deleted successfully")

