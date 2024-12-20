import pytest
import datetime
from app.logic.services.event_service import EventService
from app.persistence.repositories.event_repository import EventRepository
from app.logic.services.ceremony_service import CeremonyService
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.persistence.entities import EventEntity, CeremonyEntity, CeremonyTypeEntity
from app.logic.model_mappers import CeremonyModelMapper
from app.logic.models import Event, Ceremony, CeremonyType
from app.logic.model_mappers import EventModelMapper
from app.persistence.repositories.voting_repository import VotingRepository


@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()

@pytest.fixture
def event_entity():
    return EventEntity(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST")

@pytest.fixture
def event_model():
    return Event(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST")

@pytest.fixture
def ceremony_entity():
    return CeremonyEntity(id=1, ceremony_type_id=1, event_id=1, date=datetime.datetime.now())

@pytest.fixture
def ceremony_model():
    return Ceremony(ceremony_type=CeremonyType(id=1, name="Semifinal 1", code="SF1"))

@pytest.fixture
def ceremony_type_entity():
    return CeremonyTypeEntity(id=1, name="Semifinal 1", code="SF1")

@pytest.fixture
def ceremony_type_model():
    return CeremonyType(id=1, name="Semifinal 1", code="SF1")


def test_get_events_with_submodels(mocker, mock_session, event_entity, event_model):
    mocker.patch.object(EventRepository, 'get_events', return_value=[event_entity])
    mocker.patch.object(EventModelMapper,'map_to_event_model', return_value=event_model)

    result = EventService(mock_session).get_events(submodels=True)
    
    assert isinstance(result, list)
    assert isinstance(result[0], Event)
    assert result[0] == event_model
    EventRepository(mock_session).get_events.assert_called_once()
    EventModelMapper().map_to_event_model.assert_called_once()


def test_get_events_without_submodels(mocker, mock_session, event_entity, event_model):
    mocker.patch.object(EventRepository, 'get_events', return_value=[event_entity])
    mocker.patch.object(EventModelMapper,'map_to_event_model_without_submodels', return_value=event_model)

    result = EventService(mock_session).get_events(submodels=False)
    
    assert isinstance(result, list)
    assert isinstance(result[0], Event)
    assert result[0] == event_model
    EventRepository(mock_session).get_events.assert_called_once()
    EventModelMapper().map_to_event_model_without_submodels.assert_called_once()


def test_get_event_with_submodels(mocker, mock_session, event_entity, event_model):
    mocker.patch.object(EventRepository, 'get_event', return_value=event_entity)
    mocker.patch.object(EventModelMapper,'map_to_event_model', return_value=event_model)

    result = EventService(mock_session).get_event(id=1, year=None, submodels=True)
    
    assert isinstance(result, Event)
    assert result == event_model
    EventRepository(mock_session).get_event.assert_called_once_with(1,None)
    EventModelMapper().map_to_event_model.assert_called_once()

def test_get_event_without_submodels(mocker, mock_session, event_entity, event_model):
    mocker.patch.object(EventRepository, 'get_event', return_value=event_entity)
    mocker.patch.object(EventModelMapper,'map_to_event_model_without_submodels', return_value=event_model)

    result = EventService(mock_session).get_event(id=1, year=None, submodels=False)
    
    assert isinstance(result, Event)
    assert result == event_model
    EventRepository(mock_session).get_event.assert_called_once_with(1,None)
    EventModelMapper().map_to_event_model_without_submodels.assert_called_once()

def test_get_event_not_found(mocker, mock_session):
    mocker.patch.object(EventRepository, 'get_event', return_value=None)

    with pytest.raises(Exception) as exception:
        EventService(mock_session).get_event(id=1, year=None)
        assert exception.field == "event_id"


def test_get_event_ceremony(mocker, mock_session, ceremony_entity, ceremony_model):
    mocker.patch.object(CeremonyRepository, 'get_event_ceremony', return_value=ceremony_entity)
    mocker.patch.object(CeremonyModelMapper,'map_to_ceremony_model_without_event', return_value=ceremony_model)

    result = CeremonyService(mock_session).get_event_ceremony(ceremony_id=1, event_id=1)
    
    assert isinstance(result, Ceremony)
    assert result == ceremony_model
    CeremonyRepository(mock_session).get_event_ceremony.assert_called_once_with(ceremony_id=1, event_id=1)


def test_get_event_ceremonies(mocker, mock_session, ceremony_entity, ceremony_model):
    mocker.patch.object(CeremonyRepository, 'get_ceremonies_by_event_id', return_value=[1,2])
    mocker.patch.object(CeremonyModelMapper,'map_to_ceremony_map', return_value={1:2})

    result = CeremonyService(mock_session).get_event_ceremonies(event_id=1)

    assert isinstance(result, dict)
    assert result == {1:2}
    
    CeremonyRepository(mock_session).get_ceremonies_by_event_id.assert_called_once_with(event_id=1)


def test_get_event_ceremony_not_found(mocker, mock_session):
    mocker.patch.object(CeremonyRepository, 'get_event_ceremony', return_value=None)

    with pytest.raises(Exception) as exception:
        CeremonyService(mock_session).get_event_ceremony(ceremony_id=1, event_id=1)
        assert exception.field == "event_id,ceremony_id"

def test_get_ceremonies_with_ceremony_types_by_event_id_test(mocker, mock_session, ceremony_entity, ceremony_model):
    mocker.patch.object(CeremonyRepository, 'get_ceremonies_with_ceremony_types_by_event_id', return_value=[ceremony_entity])
    mocker.patch.object(CeremonyModelMapper, 'map_to_ceremony_model_with_ceremony_type', return_value=ceremony_model)

    result = CeremonyService(mock_session).get_ceremonies_with_ceremony_types_by_event_id(event_id=1)

    assert isinstance(result, list)
    assert isinstance(result[0], Ceremony)
    assert result[0] == ceremony_model

def test_create_event(mocker, mock_session, event_entity, event_model, ceremony_type_entity, ceremony_type_model, ceremony_entity):
    mocker.patch.object(EventModelMapper, "map_to_event_entity", return_value=event_entity)
    mocker.patch.object(EventRepository, "create_event", return_value=event_entity)
    mocker.patch.object(EventModelMapper, "map_to_event_model_without_submodels", return_value=event_model)
    mocker.patch.object(CeremonyModelMapper, "map_to_ceremony_type_model", return_value=ceremony_type_model)
    mocker.patch.object(CeremonyRepository, "get_ceremony_type", return_value=ceremony_type_entity)
    mocker.patch.object(CeremonyRepository, "create_ceremony", return_value=1)
    mocker.patch.object(CeremonyModelMapper, "map_to_ceremony_entity", return_value=ceremony_entity)

    result = EventService(mock_session).create_event_and_associated_ceremonies(event=Event(), grand_final_date=datetime.datetime.now().date())

    assert isinstance(result, Event)
    assert result == event_model



def test_create_ceremony(mocker, mock_session, ceremony_entity):

    created_ceremony_id = 1
    mocker.patch.object(CeremonyModelMapper, 'map_to_ceremony_entity', return_value=ceremony_entity)
    mocker.patch.object(CeremonyRepository, 'create_ceremony', return_value=created_ceremony_id)

    result = CeremonyService(mock_session).create_ceremony(ceremony=ceremony_entity)

    assert result == created_ceremony_id

def test_update_event(mocker, mock_session, event_model, event_entity):
    mocker.patch.object(EventRepository, "get_event", return_value=event_model)
    mocker.patch.object(VotingRepository, "check_exists_votings_by_event_id", return_value=False)
    mocker.patch.object(EventRepository, "update_event", return_value=event_entity)
    mocker.patch.object(EventModelMapper, "map_to_event_model", return_value=event_model)
    mocker.patch.object(EventModelMapper, "map_to_event_entity", return_value=event_entity)
    mocker.patch.object(EventRepository, "update_event", return_value=None)

    try:
        EventService(mock_session).update_event(event_id=1, event=event_model)
    except Exception as exception:
        pytest.fail(f"Test failed with exception: {exception}")


def test_update_event_not_found(mocker, mock_session, event_model):
    mocker.patch.object(EventRepository, "get_event", return_value=None)
    mocker.patch.object(VotingRepository, "check_exists_votings_by_event_id")

    with pytest.raises(Exception) as exception:
        EventService(mock_session).update_event(event_id=1, event=event_model)
        assert exception.field == "event_id"

    VotingRepository(mock_session).check_exists_votings_by_event_id.assert_not_called()

def test_update_simulated_event(mocker, mock_session, event_model):
    mocker.patch.object(EventRepository, "get_event", return_value=event_model)
    mocker.patch.object(VotingRepository, "check_exists_votings_by_event_id", return_value=True)

    with pytest.raises(Exception) as exception:
        EventService(mock_session).update_event(event_id=1, event=event_model)
        assert exception.field == "event_id"

    VotingRepository(mock_session).check_exists_votings_by_event_id.assert_called_once()

def test_add_songs_to_ceremony(mocker, mock_session):
    mocker.patch.object(CeremonyRepository, "add_songs_to_ceremony", return_value=None)

    try:
        CeremonyService(mock_session).add_songs_to_ceremony(ceremony_id=1, song_ids=[1,2,3])
    except Exception as exception:
        pytest.fail(f"Test failed with exception: {exception}")

def test_delete_event(mocker, mock_session, event_model):
    mocker.patch.object(EventRepository, "get_event", return_value=event_model)
    mocker.patch.object(VotingRepository, "check_exists_votings_by_event_id", return_value=False)
    mocker.patch.object(EventRepository, "delete_event", return_value=None)

    try:
        EventService(mock_session).delete_event(event_id=1)
    except Exception as exception:
        pytest.fail(f"Test failed with exception: {exception}")

def test_delete_event_not_found(mocker, mock_session):
    mocker.patch.object(EventRepository, "get_event", return_value=None)
    mocker.patch.object(VotingRepository, "check_exists_votings_by_event_id")

    with pytest.raises(Exception) as exception:
        EventService(mock_session).delete_event(event_id=1)
        assert exception.field == "event_id"

    VotingRepository(mock_session).check_exists_votings_by_event_id.assert_not_called()

def test_delete_simulated_event(mocker, mock_session, event_model):
    mocker.patch.object(EventRepository, "get_event", return_value=event_model)
    mocker.patch.object(VotingRepository, "check_exists_votings_by_event_id", return_value=True)

    with pytest.raises(Exception) as exception:
        EventService(mock_session).delete_event(event_id=1)
        assert exception.field == "event_id"

    VotingRepository(mock_session).check_exists_votings_by_event_id.assert_called_once()
