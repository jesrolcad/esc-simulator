import pytest
import strawberry
from app.logic.models import Country, Song
from app.logic.services.country_service import CountryService
from app.logic.services.song_service import SongService
from app.routers.api_mappers.country_api_mapper import CountryApiMapper
from app.routers.api_mappers.song_api_mapper import SongApiMapper
from app.routers.operations.country_operations import CountryDataResponseQL, CountryQuery, CountryMutation
from app.main import CustomContext
from app.routers.schemas.common_schemas import SongWithoutCountryCeremoniesVotingsQL
from app.tests.unit.routers.endpoints.country_endpoints_test import country_schema


@pytest.fixture
def schema():
    return strawberry.Schema(query=CountryQuery, mutation=CountryMutation)


@pytest.fixture
def context(mocker):
    return CustomContext(db=mocker.Mock())

@pytest.fixture
def country_model():
    return Country(id=1, name="test", code="COD")

@pytest.fixture
def country_schema_ql():
    return CountryDataResponseQL(id=1, name="test", code="COD")


@pytest.fixture
def song_model():
    return Song(id=1, title="test", artist="test", belongs_to_host_country=True, jury_potential_score=1, televote_potential_score=1)

@pytest.fixture
def song_schema_ql():
    return SongWithoutCountryCeremoniesVotingsQL(id=1, title="test", artist="test", belongs_to_host_country=True, jury_potential_score=1, televote_potential_score=1)


def test_countries_query(mocker, schema, context, country_model, country_schema_ql, song_model, song_schema_ql):
    mocker.patch.object(CountryService, 'get_countries', return_value=[country_model])
    mocker.patch.object(CountryDataResponseQL, 'map_to_country_data_response_ql', return_value=country_schema_ql)
    mocker.patch.object(SongService, 'get_songs_by_country_id', return_value=song_model)
    mocker.patch.object(SongApiMapper, 'map_to_song_without_country_ceremonies_votings_ql', return_value=song_schema_ql)

    query = '''
        query {
            countries {
                code
                id
                name
                songs {
                    id
                    title
                    artist
                    belongsToHostCountry
                    juryPotentialScore
                    televotePotentialScore
                
                    }
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors


def test_country_query(mocker, schema, context, country_model, country_schema_ql, song_model, song_schema_ql):
    mocker.patch.object(CountryService, 'get_country', return_value=country_model)
    mocker.patch.object(CountryDataResponseQL, 'map_to_country_data_response_ql', return_value=country_schema_ql)
    mocker.patch.object(SongService, 'get_songs_by_country_id', return_value=song_model)
    mocker.patch.object(SongApiMapper, 'map_to_song_without_country_ceremonies_votings_ql', return_value=song_schema_ql)

    query = '''
        query {
            country(countryId: 1) {
                code
                id
                name
                songs {
                    id
                    title
                    artist
                    belongsToHostCountry
                    juryPotentialScore
                    televotePotentialScore
                }
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors


def test_create_country_mutation(mocker, schema, context, country_model, country_schema_ql):
    mocker.patch.object(CountryApiMapper, 'map_country_request_ql_to_country_model', return_value=country_model)
    mocker.patch.object(CountryService, 'create_country', return_value=country_model)
    mocker.patch.object(CountryDataResponseQL, 'map_to_country_data_response_ql', return_value=country_schema_ql)

    query = '''
        mutation {
            createCountry(country: {name: "test", code: "COD"}) {
                code
                id
                name
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors


def test_update_country_mutation(mocker, schema, context, country_model, country_schema_ql):
    mocker.patch.object(CountryApiMapper, 'map_country_request_ql_to_country_model', return_value=country_model)
    mocker.patch.object(CountryService, 'update_country')
    mocker.patch.object(CountryDataResponseQL, 'map_to_country_data_response_ql', return_value=country_schema_ql)

    query = '''
        mutation {
            updateCountry(countryId: 1, country: {name: "test", code: "COD"}) {
                success
                message
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors


def test_delete_country_mutation(mocker, schema, context):
    mocker.patch.object(CountryService, 'delete_country')

    query = '''
        mutation {
            deleteCountry(countryId: 1) {
                success
                message
            }
        }
    '''

    response = schema.execute_sync(query, context_value=context)
    assert not response.errors