from fastapi import status
from app.routers.schemas.api_schemas import ErrorResponse
from app.routers.schemas.simulator_schemas import ParticipantDataResponseList, SimulationResultDataResponse, SimulationCeremonyResultDataResponse

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

get_event_ceremony_type_results_endpoint = {
    "summary": "Get results by a specific ceremony type of an event",
    "description": "Get results by a specific ceremony type of an event",
    "responses": {
        status.HTTP_200_OK: {
            "model": SimulationCeremonyResultDataResponse,
            "description": "Event ceremony type results retrieved successfully"
        }, 

        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Event not found"
        }
    }
}

create_event_simulation_endpoint = {
    "summary": "Create event simulation",
    "description": "Create event simulation",
    "responses": {
        status.HTTP_200_OK: {
            "description": "Event simulation created successfully"
        }, 

        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Event not found"
        }
    }
}

delete_event_simulation_endpoint = {
    "summary": "Delete event simulation",
    "description": "Delete event simulation",
    "responses": {
        status.HTTP_200_OK: {
            "description": "Event simulation deleted successfully"
        }, 

        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Event not found"
        }
    }
}