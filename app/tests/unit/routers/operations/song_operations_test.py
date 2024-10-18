from numpy import isin
import pytest
import strawberry
from app.logic.models import Song, Country, Event
from app.logic.services.country_service import CountryService
from app.logic.services.song_service import SongService
from app.routers.api_mappers.country_api_mapper import CountryApiMapper
from app.routers.api_mappers.song_api_mapper import SongApiMapper
from app.routers.operations.song_operations import SongDataResponseQL, SongQuery, SongMutation
from app.main import CustomContext
from app.routers.schemas.common_schemas import CountryWithoutSongsVotingsDataResponseQL

@pytest.fixture
def schema():
    return strawberry.Schema(query=SongQuery, mutation=SongMutation)

@pytest.fixture
def country_model():
    return Country(id=1, name="test", code="COD")

@pytest.fixture
def song_model(country_model):
    Song.model_rebuild()
    return Song(id=1, country_id=1, event_id=1, title="test", artist="test",
                                belongs_to_host_country=True, jury_potential_score=1, televote_potential_score=1,
                                country=country_model, event=Event(id=1, year=1, slogan="test", host_city="test", arena="test"),
                                ceremonies=[], votings=[])

@pytest.fixture
def context(mocker):
    return CustomContext(db=mocker.Mock())

@pytest.fixture
def song_schema_ql():
    return SongDataResponseQL(id=1, title="test", artist="test", belongs_to_host_country=True, jury_potential_score=1, televote_potential_score=1)

@pytest.fixture
def country_ql_schema():
    return CountryWithoutSongsVotingsDataResponseQL(id=1, name="test", code="COD")

def test_songs_query(mocker, schema, context, song_model, song_schema_ql, country_ql_schema):
    mocker.patch.object(SongService, 'get_songs', return_value=[song_model])
    mocker.patch.object(CountryService, 'get_country_by_song_id', return_value=song_model.country)
    mocker.patch.object(CountryApiMapper, 'map_to_country_without_songs_votings_data_response_ql', return_value=country_ql_schema)
    mocker.patch.object(SongDataResponseQL, 'map_to_song_data_response_ql', return_value=song_schema_ql)

    query = '''
        query {
            songs {
                id
                title
                artist
                belongsToHostCountry
                juryPotentialScore
                televotePotentialScore
                country {
                    id
                    name
                    code
                }
                summary
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors

def test_song_query(mocker, schema, context, song_model, song_schema_ql, country_ql_schema):
    mocker.patch.object(SongService, 'get_song', return_value=song_model)
    mocker.patch.object(CountryService, 'get_country_by_song_id', return_value=song_model.country)
    mocker.patch.object(CountryApiMapper, 'map_to_country_without_songs_votings_data_response_ql', return_value=country_ql_schema)
    mocker.patch.object(SongDataResponseQL, 'map_to_song_data_response_ql', return_value=song_schema_ql)

    query = '''
        query {
            song(songId: 1) {
                id
                title
                artist
                belongsToHostCountry
                juryPotentialScore
                televotePotentialScore
                country {
                    id
                    name
                    code
                }
                summary
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors

def test_create_song_mutation(mocker, schema, context, song_model, song_schema_ql):
    mocker.patch.object(SongApiMapper, 'map_song_request_ql_to_song_model', return_value=song_model)
    mocker.patch.object(SongService, 'create_song', return_value=song_model)
    mocker.patch.object(SongDataResponseQL, 'map_to_song_data_response_ql', return_value=song_schema_ql)

    query = '''
        mutation {
            createSong(song: { title: "test", artist: "test", countryId: 1, eventId: 1, belongsToHostCountry: true, juryPotentialScore: ONE, televotePotentialScore: ONE}) {
                id
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors


def test_update_song_mutation(mocker, schema, context, song_model):
    mocker.patch.object(SongApiMapper, 'map_song_request_ql_to_song_model', return_value=song_model)
    mocker.patch.object(SongService, 'update_song')

    query = '''
        mutation {
            updateSong(songId: 1, song: { title: "test", artist: "test", countryId: 1, eventId: 1, belongsToHostCountry: true, juryPotentialScore: ONE, televotePotentialScore: ONE}) {
                success
                message
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors

def test_delete_song_mutation(mocker, schema, context):
    mocker.patch.object(SongService, 'delete_song')

    query = '''
        mutation {
            deleteSong(songId: 1) {
                success
                message
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors