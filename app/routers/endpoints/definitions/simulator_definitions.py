from fastapi import status
from app.routers.schemas.simulator_schemas import ParticipantDataResponseList

get_event_ceremony_participants_endpoint = {
    "summary": "Get event ceremony participants",
    "description": "Get event ceremony participants",
    "responses": {
        status.HTTP_200_OK: {
            "model": ParticipantDataResponseList,
            "description": "Get event ceremony participants"
        }
    }
}