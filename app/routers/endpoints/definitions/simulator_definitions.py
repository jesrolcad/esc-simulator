from fastapi import status
from app.routers.schemas.simulator_schemas import ParticipantDataResponseList, SimulationResultDataResponse

get_event_ceremony_participants_endpoint = {
    "summary": "Get event ceremony participants",
    "description": "Get event ceremony participants",
    "responses": {
        status.HTTP_200_OK: {
            "model": ParticipantDataResponseList,
            "description": "Event ceremony participants retrieved successfully"
        }
    }
}


get_event_results_endpoint = {
    "summary": "Get event results",
    "description": "Get event results",
    "responses": {
        status.HTTP_200_OK: {
            "model": SimulationResultDataResponse,
            "description": "Event results retrieved successfully"
        }
    }
}