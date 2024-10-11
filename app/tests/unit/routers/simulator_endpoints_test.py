import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.logic.models import CeremonyType, Participant, SimulationCeremonyResult
from app.logic.services.simulator_service import SimulatorService
from app.main import app
from app.routers.api_mappers.simulator_api_mapper import SimulatorApiMapper
from app.routers.schemas.api_schemas import ResultResponse
from app.routers.schemas.simulator_schemas import ParticipantDataResponse, SimulationCeremonyResultDataResponse, ParticipantResultDataResponseList


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def participant_model():
    return Participant(country_id=1, song_id=1, participant_info="Spain. Amaia y Alfred - Tu Canción. Jury potential score: 4 | Televote potential score: 2")

@pytest.fixture
def participant_schema():
    return ParticipantDataResponse(country_id=1, song_id=1, participant_info="Spain. Amaia y Alfred - Tu Canción. Jury potential score: 4 | Televote potential score: 2")

@pytest.fixture
def simulation_ceremony_result_model():
    return SimulationCeremonyResult(ceremony_id=1, ceremony_type=CeremonyType(id=1, name="Semifinal 1", code="SF1"))

@pytest.fixture
def simulation_ceremony_result_schema():
    return SimulationCeremonyResultDataResponse(ceremony_id=1, ceremony_type_id=1, ceremony_type_name="Semifinal 1", results=ParticipantResultDataResponseList(participants=[]))


def test_get_event_ceremony_participants(mocker,client, participant_model, participant_schema):

    mocker.patch.object(SimulatorService, 'get_simulation_participants_by_event_ceremony', return_value=[participant_model])
    mocker.patch.object(SimulatorApiMapper, 'map_to_participant_data_response', return_value=participant_schema)

    response = client.get("/simulator/events/1/ceremonies/1/participants")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [participant_schema.model_dump()]


def test_get_event_results(mocker, client):

    mocker.patch.object(SimulatorService, 'get_simulation_event_results', return_value=[])
    mocker.patch.object(SimulatorApiMapper, 'map_to_simulator_ceremony_data_response_list', return_value=[])

    response = client.get("/simulator/events/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_event_ceremony_type_results(mocker, client, simulation_ceremony_result_model, simulation_ceremony_result_schema):

    mocker.patch.object(SimulatorService, 'get_simulation_event_results_by_ceremony_type', return_value=simulation_ceremony_result_model)
    mocker.patch.object(SimulatorApiMapper, 'map_to_simulator_ceremony_data_response', return_value=simulation_ceremony_result_schema)

    response = client.get("/simulator/events/1/ceremony-types/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == simulation_ceremony_result_schema.model_dump()


def test_create_event_simulation(mocker, client):

    mocker.patch.object(SimulatorService, 'create_simulation', return_value=None)

    response = client.post("/simulator/events/1/simulate")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == ResultResponse(message="Event simulated successfully").model_dump()


def test_delete_event_simulation(mocker, client):
    
    mocker.patch.object(SimulatorService, 'delete_simulation_by_event_id', return_value=None)
    
    response = client.delete("/simulator/events/1")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == ResultResponse(message="Event simulation deleted successfully").model_dump()