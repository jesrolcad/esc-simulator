import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.logic.models import Participant
from app.logic.services.simulator_service import SimulatorService
from app.main import app
from app.routers.api_mappers.simulator_api_mapper import SimulatorApiMapper
from app.routers.schemas.simulator_schemas import ParticipantDataResponse


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def participant_model():
    return Participant(country_id=1, song_id=1, participant_info="Spain. Amaia y Alfred - Tu Canción. Jury potential score: 4 | Televote potential score: 2")

@pytest.fixture
def participant_schema():
    return ParticipantDataResponse(country_id=1, song_id=1, participant_info="Spain. Amaia y Alfred - Tu Canción. Jury potential score: 4 | Televote potential score: 2")

@pytest.mark.asyncio
def test_get_event_ceremony_participants(mocker,client, participant_model, participant_schema):

    mocker.patch.object(SimulatorService, 'get_simulation_participants_by_event_ceremony', return_value=[participant_model])
    mocker.patch.object(SimulatorApiMapper, 'map_to_participant_data_response', return_value=participant_schema)

    response = client.get("/simulator/events/1/ceremonies/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [participant_schema.model_dump()]


