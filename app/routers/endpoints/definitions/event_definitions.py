from fastapi import status
from app.routers.schemas.event_schemas import EventDataResponseList

get_events_endpoint = {
    "summary": "Get all events",
    "description": "Get all events",
    "responses": {
        status.HTTP_200_OK: {
            "model": EventDataResponseList,
            "description": "Events retrieved successfully"
        }
    }
}

get_event_endpoint = {
    "summary": "Get event by id",
    "description": "Get event by id",
    "responses": {
        status.HTTP_200_OK: {
            "model": EventDataResponseList,
            "description": "Event retrieved successfully"
        }
    }
}

get_event_ceremony_endpoint =  {
    "summary": "Get event ceremony",
    "description": "Get event ceremony by event id and ceremony id",
    "responses": {
        status.HTTP_200_OK: {
            "model": EventDataResponseList,
            "description": "Event ceremonies retrieved successfully"
        }
    }
}