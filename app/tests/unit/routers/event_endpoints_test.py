import pytest
from fastapi.testclient import TestClient
from app.logic.services.event_service import EventService
from app.logic.models import Event
from app.main import app
from app.routers.api_mappers.event_api_mapper import EventApiMapper
from app.routers.schemas.event_schemas import EventDataResponse

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def event_model():
    return Event(id=1, year=2023, slogan="TEST", host_city="TEST", arena="TEST")

@pytest.fixture
def event_schema():
    return EventDataResponse(id=1, year=2023, slogan="TEST", host_city="TEST", arena="TEST")


@pytest.mark.asyncio
async def test_get_events(mocker, client, event_model, event_schema):
    
    mocker.patch.object(EventService, "get_events", return_value=[event_model])
    mocker.patch.object(EventApiMapper, "map_to_event_data_response", return_value=event_schema)

    response = client.get("/events")

    assert response.status_code == 200
    assert response.json() == [event_schema.__dict__]
