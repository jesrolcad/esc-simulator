import pytest
from app.logic.services.song_service import SongService
from app.persistence.repositories.song_repository import SongRepository
from app.logic.models import Song, Country, Event
from app.persistence.entities import SongEntity
from app.utils.exceptions import NotFoundError


@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()


@pytest.fixture
def song_entity():

    return SongEntity(id=1, country_id=1, event_id=1, title="test", artist="test",
                            belongs_to_host_country=False, jury_potential_score=1, televote_potential_score=1,
                            country=None, event=None, ceremonies=[], votings=[])


@pytest.fixture
def song_model():
    Song.update_forward_refs()
    return Song(id=1, country_id=1, event_id=1, title="test", artist="test",
                                belongs_to_host_country=False, jury_potential_score=1, televote_potential_score=1,
                                country=Country(id=1, name="test", code="COD"), event=Event(id=1, year=1, slogan="test", host_city="test", arena="test"),
                                ceremonies=[], votings=[])

def test_get_song(mocker, mock_session, song_entity, song_model):

    mocker.patch.object(SongRepository, 'get_song', return_value=song_entity)
    mocker.patch('app.logic.model_mappers.song_model_mapper.map_to_song_model', return_value=song_model)

    song_id = 1
    result = SongService(mock_session).get_song(song_id)
    
    assert isinstance(result, Song)
    assert result == song_model
    
    SongRepository(mock_session).get_song.assert_called_once_with(song_id)


def test_get_song_exception(mocker, mock_session):

    mocker.patch.object(SongRepository, 'get_song', return_value=None)

    song_id = 1

    with pytest.raises(NotFoundError) as e:
        SongService(mock_session).get_song(song_id)


