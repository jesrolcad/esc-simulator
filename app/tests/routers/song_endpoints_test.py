import pytest
from fastapi.testclient import TestClient
from app.logic.services.song_service import SongService
from app.routers.api_mappers.song_api_mapper import SongApiMapper
from app.routers.schemas.song_schemas import SongDataResponse
from app.routers.schemas.country_schemas import CountryWithoutSongsVotingsDataResponse
from app.logic.models import Song, Country, Event
from app.utils.exceptions import NotFoundError
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()

@pytest.fixture
def song_schema():

    country = CountryWithoutSongsVotingsDataResponse(id=1, name="test", code="COD")


    return SongDataResponse(id=1, title="test", artist="test",
                            belongs_to_host_country=True, jury_potential_score=1,
                            televote_potential_score=1, country=country)

@pytest.fixture
def song_model():
    Song.update_forward_refs()
    return Song(id=1, country_id=1, event_id=1, title="test", artist="test",
                                belongs_to_host_country=True, jury_potential_score=1, televote_potential_score=1,
                                country=Country(id=1, name="test", code="COD"), event=Event(id=1, year=1, slogan="test", host_city="test", arena="test"),
                                ceremonies=[], votings=[])

@pytest.mark.asyncio
async def test_get_song_by_id(mocker, client, song_schema, song_model):

    mocker.patch.object(SongService, 'get_song', return_value=song_model)
    mocker.patch.object(SongApiMapper, 'map_to_song_data_response', return_value=song_schema)

    song_id = 1
    response = client.get(f"/songs/{song_id}")

    assert response.status_code == 200
    assert response.json() == song_schema.__dict__


@pytest.mark.asyncio
async def test_get_song_by_id_exception(mocker, client):

    mocker.patch.object(SongService, 'get_song', side_effect=NotFoundError)

    song_id = 1
    response = client.get(f"/songs/{song_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_songs(mocker, client, song_schema, song_model):
    
    mocker.patch.object(SongService, 'get_songs', return_value=[song_model])
    mocker.patch.object(SongApiMapper, 'map_to_song_data_response', return_value=song_schema)

    response = client.get("/songs")

    assert response.status_code == 200
    assert response.json() == [song_schema.__dict__]
