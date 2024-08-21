from fastapi import APIRouter, Depends
from app.db.database import get_db 
from app.logic.services.simulator_service import SimulatorService
from app.routers.api_mappers.simulator_api_mapper import SimulatorApiMapper
from .definitions.simulator_definitions import get_event_ceremony_participants_endpoint, get_event_results_endpoint, get_event_ceremony_type_results_endpoint


router = APIRouter(prefix="/simulator", tags=["simulator"])

@router.get(path="/events/{event_id}/ceremonies/{ceremony_id}/participants", summary=get_event_ceremony_participants_endpoint["summary"], description=get_event_ceremony_participants_endpoint["description"], 
            responses=get_event_ceremony_participants_endpoint["responses"])
async def get_event_ceremony_participants(event_id: int, ceremony_id: int, db: get_db = Depends()):

    response = SimulatorService(db).get_simulation_participants_by_event_ceremony(event_id=event_id, ceremony_id=ceremony_id)

    return [SimulatorApiMapper().map_to_participant_data_response(participant_model=participant_model) for participant_model in response]


@router.get(path="/events/{event_id}", summary=get_event_results_endpoint["summary"], description=get_event_results_endpoint["description"],
            responses=get_event_results_endpoint["responses"])
async def get_event_results(event_id: int, db: get_db = Depends()):
        
    response = SimulatorService(db).get_simulation_event_results(event_id=event_id)
    
    return SimulatorApiMapper().map_to_simulator_ceremony_data_response_list(simulation_result_model=response)


@router.get(path="/events/{event_id}/ceremony-types/{ceremony_type_id}", summary=get_event_ceremony_type_results_endpoint["summary"], 
            description=get_event_ceremony_type_results_endpoint["description"], responses=get_event_ceremony_type_results_endpoint["responses"])
async def get_event_ceremony_type_results(event_id: int, ceremony_type_id: int, db: get_db = Depends()):

    response = SimulatorService(db).get_simulation_event_results_by_ceremony_type(event_id=event_id, ceremony_type_id=ceremony_type_id)
    
    return SimulatorApiMapper().map_to_simulator_ceremony_data_response(simulation_result_model=response)



