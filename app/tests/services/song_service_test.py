import pytest
from app.logic.services.song_service import SongService
from app.persistence.repositories.song_repository import SongRepository
from app.persistence.repositories.country_repository import CountryRepository
from app.persistence.repositories.event_repository import EventRepository
from app.logic.models import Song, Country, Event
from app.logic.model_mappers.song_model_mapper import SongModelMapper
from app.persistence.entities import SongEntity, CountryEntity, EventEntity
from app.utils.exceptions import NotFoundError, BusinessLogicValidationError

@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()


@pytest.fixture
def song_entity():

    return SongEntity(id=1, country_id=1, event_id=1, title="test", artist="test",
                            belongs_to_host_country=True, jury_potential_score=1, televote_potential_score=1,
                            country=None, event=None, ceremonies=[], votings=[])

@pytest.fixture
def country_entity():

    return CountryEntity(id=1, name="test", code="COD", songs=[], votings=[])


@pytest.fixture
def event_entity():

    return EventEntity(id=1, year=1, slogan="test", host_city="test", arena="test", ceremonies=[])


@pytest.fixture
def song_model():
    Song.update_forward_refs()
    return Song(id=1, country_id=1, event_id=1, title="test", artist="test",
                                belongs_to_host_country=False, jury_potential_score=1, televote_potential_score=1,
                                country=Country(id=1, name="test", code="COD"), event=Event(id=1, year=1, slogan="test", host_city="test", arena="test"),
                                ceremonies=[], votings=[])

def test_get_song(mocker, mock_session, song_entity, song_model):

    mocker.patch.object(SongRepository, 'get_song', return_value=song_entity)
    mocker.patch.object(SongModelMapper, 'map_to_song_model', return_value=song_model)

    song_id = 1
    result = SongService(mock_session).get_song(song_id)
    
    assert isinstance(result, Song)
    assert result == song_model
    
    SongRepository(mock_session).get_song.assert_called_once_with(song_id)


def test_get_song_exception(mocker, mock_session):

    mocker.patch.object(SongRepository, 'get_song', return_value=None)

    song_id = 1

    with pytest.raises(NotFoundError) as exception:
        SongService(mock_session).get_song(song_id)
        assert exception.field == "song_id"


def test_get_songs(mocker, mock_session, song_entity, song_model):
    
    mocker.patch.object(SongRepository, 'get_songs', return_value=[song_entity])
    mocker.patch.object(SongModelMapper,'map_to_song_model', return_value=song_model)

    result = SongService(mock_session).get_songs(title="test", country_code="COD", event_year=1)
    
    assert isinstance(result, list)
    assert isinstance(result[0], Song)
    assert result[0] == song_model
    SongRepository(mock_session).get_songs.assert_called_once()


def test_create_song(mocker, mock_session, song_model, song_entity, country_entity, event_entity):

    mocker.patch.object(SongModelMapper, 'map_to_song_entity', return_value=song_entity)
    mocker.patch.object(SongRepository, 'check_existing_song_marked_as_belongs_to_host_country', return_value=None)
    mocker.patch.object(CountryRepository, 'get_country', return_value=country_entity)
    mocker.patch.object(EventRepository, 'get_event', return_value=event_entity)
    mocker.patch.object(SongRepository, 'get_song_by_country_and_event_id', return_value=None)
    mocker.patch.object(SongRepository, 'create_song', return_value=song_entity)
    mocker.patch.object(SongModelMapper, 'map_to_song_model', return_value=song_model)

    result = SongService(mock_session).create_song(song_model)

    assert isinstance(result, Song)
    assert result == song_model

def test_create_song_another_song_marked_as_belongs_to_host_country(mocker, mock_session, song_model, song_entity, country_entity, event_entity):

    mocker.patch.object(SongModelMapper, 'map_to_song_entity', return_value=song_entity)
    mocker.patch.object(CountryRepository, 'get_country', return_value=country_entity)
    mocker.patch.object(EventRepository, 'get_event', return_value=event_entity)
    mocker.patch.object(SongRepository, 'get_song_by_country_and_event_id', return_value=None)
    mocker.patch.object(SongRepository, 'check_existing_song_marked_as_belongs_to_host_country', return_value=1)

    with pytest.raises(BusinessLogicValidationError) as exception:
        SongService(mock_session).create_song(song_model)
        assert exception.field == "belongs_to_host_country"

@pytest.mark.parametrize("country_id, event_id", [(None, 1), (1, None), (None, None)])
def test_create_song_country_event_not_exist(mocker, mock_session, song_model, song_entity, country_id, event_id):

    mocker.patch.object(SongModelMapper, 'map_to_song_entity', return_value=song_entity)
    mocker.patch.object(CountryRepository, 'get_country', return_value=country_id)
    mocker.patch.object(EventRepository, 'get_event', return_value=event_id)
    
    with pytest.raises(BusinessLogicValidationError) as exception:
        SongService(mock_session).create_song(song_model)
        assert exception.field == "country_id" or exception.field == "event_id" or exception.field == "country_id, event_id"


def test_create_song_song_already_exist_for_combination_country_and_event(mocker, mock_session, song_model, song_entity, country_entity, event_entity):
    mocker.patch.object(SongModelMapper, 'map_to_song_entity', return_value=song_entity)
    mocker.patch.object(CountryRepository, 'get_country', return_value=country_entity)
    mocker.patch.object(EventRepository, 'get_event', return_value=event_entity)
    mocker.patch.object(SongRepository, 'get_song_by_country_and_event_id', return_value=song_entity)

    with pytest.raises(BusinessLogicValidationError) as exception:
        SongService(mock_session).create_song(song_model)
        assert exception.field == "country_id, event_id"

def test_update_song(mocker, mock_session, song_model, song_entity, country_entity, event_entity):

    mocker.patch.object(SongRepository, 'get_song', return_value=song_entity)
    mocker.patch.object(SongModelMapper, 'map_to_song_entity', return_value=song_entity)
    mocker.patch.object(CountryRepository, 'get_country', return_value=country_entity)
    mocker.patch.object(EventRepository, 'get_event', return_value=event_entity)
    mocker.patch.object(SongRepository, 'get_song_by_country_and_event_id', return_value=None)
    mocker.patch.object(SongRepository, 'check_existing_song_marked_as_belongs_to_host_country', return_value=None)
    mocker.patch.object(SongModelMapper, 'map_to_song_model', return_value=song_model)
    mocker.patch.object(SongRepository, 'update_song', return_value=song_entity)

    song_id = 1

    result = SongService(mock_session).update_song(song_id=song_id,updated_song=song_model)

    assert isinstance(result, Song)
    assert result == song_model
    assert result.id == song_id

def test_update_song_song_not_exist(mocker, mock_session, song_model):

    mocker.patch.object(SongRepository, 'get_song', side_effect=NotFoundError)

    song_id = 1

    with pytest.raises(NotFoundError) as exception:
        SongService(mock_session).update_song(song_id=song_id,updated_song=song_model)
        assert exception.field == "song_id"

@pytest.mark.parametrize("country_id, event_id", [(None, 1), (1, None), (None, None)])
def test_update_song_country_event_not_exist(mocker, mock_session, song_model, song_entity, country_id, event_id):

    mocker.patch.object(SongRepository, 'get_song', return_value=song_entity)
    mocker.patch.object(SongModelMapper, 'map_to_song_model', return_value=song_model)
    mocker.patch.object(SongModelMapper, 'map_to_song_entity', return_value=song_entity)
    mocker.patch.object(CountryRepository, 'get_country', return_value=country_id)
    mocker.patch.object(EventRepository, 'get_event', return_value=event_id)

    song_id = 1
    
    with pytest.raises(BusinessLogicValidationError) as exception:
        SongService(mock_session).update_song(song_id=song_id,updated_song=song_model)
        assert exception.field == "country_id" or exception.field == "event_id" or exception.field == "country_id, event_id"


def test_update_song_song_already_exist_for_combination_country_and_event(mocker, mock_session, song_model, song_entity, country_entity, event_entity):

    mocker.patch.object(SongRepository, 'get_song', return_value=song_entity)
    mocker.patch.object(SongModelMapper, 'map_to_song_model', return_value=song_model)
    mocker.patch.object(SongModelMapper, 'map_to_song_entity', return_value=song_entity)
    mocker.patch.object(CountryRepository, 'get_country', return_value=country_entity)
    mocker.patch.object(EventRepository, 'get_event', return_value=event_entity)
    mocker.patch.object(SongRepository, 'get_song_by_country_and_event_id', return_value=song_entity)

    song_id = 1

    with pytest.raises(BusinessLogicValidationError) as exception:
        SongService(mock_session).update_song(song_id=song_id,updated_song=song_model)
        assert exception.field == "country_id, event_id"

def test_update_song_another_song_marked_as_belongs_to_host_country(mocker, mock_session, song_model, song_entity, country_entity, event_entity):
    mocker.patch.object(SongRepository, 'get_song', return_value=song_entity)
    mocker.patch.object(SongModelMapper, 'map_to_song_model', return_value=song_model)
    mocker.patch.object(SongModelMapper, 'map_to_song_entity', return_value=song_entity)
    mocker.patch.object(CountryRepository, 'get_country', return_value=country_entity)
    mocker.patch.object(EventRepository, 'get_event', return_value=event_entity)
    mocker.patch.object(SongRepository, 'get_song_by_country_and_event_id', return_value=song_entity)
    mocker.patch.object(SongRepository, 'check_existing_song_marked_as_belongs_to_host_country', return_value=1)

    song_id = 1

    with pytest.raises(BusinessLogicValidationError) as exception:
        SongService(mock_session).update_song(song_id=song_id,updated_song=song_model)
        assert exception.field == 'belongs_to_host_country'

