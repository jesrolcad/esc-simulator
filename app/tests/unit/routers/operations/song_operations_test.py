import pytest
import strawberry
from app.logic.models import Song, Country, Event
from app.logic.services.song_service import SongService
from app.routers.operations.song_operations import SongDataResponseQL, SongQuery, SongMutation
from app.main import CustomContext

@pytest.fixture
def schema():
    return strawberry.Schema(query=SongQuery, mutation=SongMutation)

@pytest.fixture
def song_model():
    Song.model_rebuild()
    return Song(id=1, country_id=1, event_id=1, title="test", artist="test",
                                belongs_to_host_country=True, jury_potential_score=1, televote_potential_score=1,
                                country=Country(id=1, name="test", code="COD"), event=Event(id=1, year=1, slogan="test", host_city="test", arena="test"),
                                ceremonies=[], votings=[])

@pytest.fixture
def context(mocker):
    return CustomContext(db=mocker.Mock())

@pytest.fixture
def song_schema_ql():
    return SongDataResponseQL(id=1, title="test", artist="test", belongs_to_host_country=True, jury_potential_score=1, televote_potential_score=1)

def test_songs_query(mocker, schema, context, song_model, song_schema_ql):
    mocker.patch.object(SongService, 'get_songs', return_value=[song_model])
    mocker.patch.object(SongDataResponseQL, 'map_to_song_data_response_ql', return_value=song_schema_ql)

    query = '''
        query {
            songs {
                id
                title
                artist
                juryPotentialScore
                televotePotentialScore
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors