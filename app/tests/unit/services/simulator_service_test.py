from ast import List
import datetime
import pytest

from app.logic.models import Ceremony, CeremonyType, Country, Participant, Song
from app.logic.services.simulator_service import SimulatorService
from app.persistence.entities import CeremonyEntity
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.model_mappers import CeremonyModelMapper

@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()

@pytest.fixture
def participant_model():
    return Participant(country_id=1, song_id=1, participant_info="Italy. Måneskin - Zitti e buoni. Jury potential score: 10 | Televote potential score: 9")


@pytest.fixture
def ceremony_entity():
    return CeremonyEntity(id=1, ceremony_type_id=1, event_id=1, date=datetime.datetime.now())

@pytest.fixture
def ceremony_model():
    country = Country(id=1, name="Italy", code="ITA")
    song = Song(id=1, title="Zitti e buoni", artist="Måneskin", jury_potential_score=10, televote_potential_score=9, belongs_to_host_country=False, country=country)
    return Ceremony(ceremony_type=CeremonyType(id=1, name="Semifinal 1", code="SF1"), songs=[song])


def test_get_event_ceremony_participants(mocker, mock_session, ceremony_entity, ceremony_model, participant_model):

    mocker.patch.object(CeremonyRepository, 'get_event_ceremony', return_value=ceremony_entity)
    mocker.patch.object(CeremonyModelMapper,'map_to_ceremony_model_without_event', return_value=ceremony_model)

    result = SimulatorService(mock_session).get_simulation_participants_by_event_ceremony(event_id=1, ceremony_id=1)

    assert isinstance(result, list)
    assert result[0] == participant_model



    
    



