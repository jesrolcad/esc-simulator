import datetime
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.logic.services.event_service import EventService
from app.logic.services.ceremony_service import CeremonyService
from app.logic.models import Event, Ceremony, CeremonyType
from app.main import app
from app.routers.api_mappers.event_api_mapper import EventApiMapper
from app.routers.api_mappers.ceremony_api_mapper import CeremonyApiMapper
from app.routers.schemas.event_schemas import EventDataResponse, EventRequest
from app.routers.schemas.common_schemas import CeremonyWithoutEventDataResponse, CeremonyTypeDataResponse
from app.utils.exceptions import NotFoundError



@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def event_model():
    return Event(id=1, year=2023, slogan="TEST", host_city="TEST", arena="TEST")

@pytest.fixture
def event_schema():
    return EventDataResponse(id=1, year=2023, slogan="TEST", host_city="TEST", arena="TEST")

@pytest.fixture
def event_ceremony_model():
    return Ceremony(ceremony_type=CeremonyType(name="Semifinal 1",code="Semifinal 1"), date=datetime.datetime.now(), event=Event(id=1, year=2023, slogan="TEST", host_city="TEST", arena="TEST"))

@pytest.fixture
def event_ceremony_schema():
    return CeremonyWithoutEventDataResponse(id=1, ceremony_type=CeremonyTypeDataResponse(id=1,name="Semifinal 1", code="SF1"), date=datetime.datetime.now().date())

@pytest.fixture
def event_request_schema():
    return EventRequest(year=2023, slogan="TEST", host_city="TEST", arena="TEST", grand_final_date=datetime.datetime.now().date())



@pytest.mark.asyncio
async def test_get_events(mocker, client, event_model, event_schema):
    
    mocker.patch.object(EventService, "get_events", return_value=[event_model])
    mocker.patch.object(EventApiMapper, "map_to_event_data_response", return_value=event_schema)

    response = client.get("/events")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [event_schema.__dict__]


@pytest.mark.asyncio
async def test_get_event(mocker, client, event_model, event_schema):
    
    mocker.patch.object(EventService, "get_event", return_value=event_model)
    mocker.patch.object(EventApiMapper, "map_to_event_data_response", return_value=event_schema)

    response = client.get("/events/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == event_schema.__dict__


@pytest.mark.asyncio
async def test_get_event_not_found(mocker, client):

    mocker.patch.object(EventService, "get_event", side_effect=NotFoundError)

    response = client.get("/events/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_event_ceremony(mocker, client, event_ceremony_model, event_ceremony_schema):
    
    mocker.patch.object(CeremonyService, "get_event_ceremony", return_value=event_ceremony_model)
    mocker.patch.object(CeremonyApiMapper, "map_to_ceremony_without_event_data_response", return_value=event_ceremony_schema)

    response = client.get("/events/1/ceremonies/1")

    assert response.status_code == status.HTTP_200_OK
    assert CeremonyWithoutEventDataResponse(**response.json()) == event_ceremony_schema

@pytest.mark.asyncio
async def test_get_event_ceremony_not_found(mocker, client):

    mocker.patch.object(CeremonyService, "get_event_ceremony", side_effect=NotFoundError)

    response = client.get("/events/1/ceremonies/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_event(mocker, client, event_model, event_request_schema):
    mocker.patch.object(EventApiMapper, "map_to_event_model", return_value=event_model)
    mocker.patch.object(EventService, "create_event_and_associated_ceremonies", return_value=event_model)

    request = event_request_schema.model_dump(mode='json')
    request['grand_final_date'] = "2023-05-13"

    response = client.post("/events", json=request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['data']['id'] == 1