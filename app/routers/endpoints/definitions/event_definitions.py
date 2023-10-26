from fastapi import status
from app.routers.schemas.event_schemas import EventDataResponseList
from app.routers.schemas.api_schemas import ErrorResponse, ResultResponse

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

create_event_endpoint = {
    "summary": "Create event",
    "description": "Create event. Ceremonies for Semi-Final 1, Semi-Final 2 and Grand Final will be created automatically.",
    "responses": {
        status.HTTP_201_CREATED: {
            "model": ResultResponse,
            "description": "Event created successfully"
        },

        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid request body"
        }
    }
}