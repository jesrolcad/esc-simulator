import pytest
from app.logic.services.event_service import EventService
from app.persistence.repositories.event_repository import EventRepository
from app.persistence.entities import EventEntity
from app.logic.models import Event
from app.logic.model_mappers import EventModelMapper


@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()

@pytest.fixture
def event_entity():
    return Event(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST")

@pytest.fixture
def event_model():
    return Event(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST")


def test_get_events(mocker, mock_session, event_entity, event_model):
    mocker.patch.object(EventRepository, 'get_events', return_value=[event_entity])
    mocker.patch.object(EventModelMapper,'map_to_event_model', return_value=event_model)

    result = EventService(mock_session).get_events()
    
    assert isinstance(result, list)
    assert isinstance(result[0], Event)
    assert result[0] == event_model
    EventRepository(mock_session).get_events.assert_called_once()