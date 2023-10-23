from fastapi import APIRouter, Depends
from app.db.database import get_db 
from app.routers.endpoints.definitions.event_definitions import get_events_endpoint
from app.logic.services.event_service import EventService
from app.routers.api_mappers.event_api_mapper import EventApiMapper



router = APIRouter(prefix="/events", tags=["events"])


@router.get(path="", summary=get_events_endpoint["summary"], description=get_events_endpoint["description"], 
            responses=get_events_endpoint["responses"])
async def get_events(db: get_db = Depends()):

    response = EventService(db).get_events()
    return [EventApiMapper().map_to_event_data_response(event) for event in response]

