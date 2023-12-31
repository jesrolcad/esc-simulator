from fastapi import APIRouter, Depends
from app.db.database import get_db 
from app.logic.services.simulator_service import SimulatorService
from app.routers.api_mappers.simulator_api_mapper import SimulatorApiMapper
from .definitions.simulator_definitions import get_event_ceremony_participants_endpoint


router = APIRouter(prefix="/simulator", tags=["simulator"])

@router.get(path="/events/{event_id}/ceremonies/{ceremony_id}/participants", summary=get_event_ceremony_participants_endpoint["summary"], description=get_event_ceremony_participants_endpoint["description"], 
            responses=get_event_ceremony_participants_endpoint["responses"])
async def get_event_ceremony_participants(event_id: int, ceremony_id: int, db: get_db = Depends()):

    response = SimulatorService(db).get_simulation_participants_by_event_ceremony(event_id=event_id, ceremony_id=ceremony_id)

    return [SimulatorApiMapper().map_to_participant_data_response(participant_model=participant_model) for participant_model in response]


