import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.logic.services.song_service import SongService
from app.routers.api_mappers.song_api_mapper import SongApiMapper
from app.routers.schemas.song_schemas import SongDataResponse, SongRequest
from app.routers.schemas.common_schemas import CountryWithoutSongsVotingsDataResponse
from app.logic.models import Song, Country, Event
from app.utils.exceptions import NotFoundError, BusinessLogicValidationError
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def song_schema():

    country = CountryWithoutSongsVotingsDataResponse(id=1, name="test", code="COD")


    return SongDataResponse(id=1, title="test", artist="test",
                            belongs_to_host_country=True, jury_potential_score=1,
                            televote_potential_score=1, country=country)

@pytest.fixture
def song_model():
    Song.model_rebuild()
    return Song(id=1, country_id=1, event_id=1, title="test", artist="test",
                                belongs_to_host_country=True, jury_potential_score=1, televote_potential_score=1,
                                country=Country(id=1, name="test", code="COD"), event=Event(id=1, year=1, slogan="test", host_city="test", arena="test"),
                                ceremonies=[], votings=[])

@pytest.fixture
def song_request_schema():
    return SongRequest(title="test", artist="test", belongs_to_host_country=True, 
                            jury_potential_score=1, televote_potential_score=1, country_id=1, event_id=1)


@pytest.mark.asyncio
async def test_get_song_by_id(mocker, client, song_schema, song_model):

    mocker.patch.object(SongService, 'get_song', return_value=song_model)
    mocker.patch.object(SongApiMapper, 'map_to_song_data_response', return_value=song_schema)

    song_id = 1
    response = client.get(f"/songs/{song_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == song_schema.__dict__


@pytest.mark.asyncio
async def test_get_song_by_id_exception(mocker, client):

    mocker.patch.object(SongService, 'get_song', side_effect=NotFoundError)

    song_id = 1
    response = client.get(f"/songs/{song_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_songs(mocker, client, song_schema, song_model):
    
    mocker.patch.object(SongService, 'get_songs', return_value=[song_model])
    mocker.patch.object(SongApiMapper, 'map_to_song_data_response', return_value=song_schema)

    response = client.get("/songs")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [song_schema.__dict__]


@pytest.mark.asyncio
async def test_create_song(mocker, client, song_request_schema, song_model):

    mocker.patch.object(SongApiMapper, 'map_to_song_model', return_value=song_model)
    mocker.patch.object(SongService, 'create_song', return_value=song_model)

    response = client.post("/songs", json=song_request_schema.dict())

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_song_exception(mocker, client, song_request_schema):
    
    mocker.patch.object(SongApiMapper, 'map_to_song_model', return_value=None)
    mocker.patch.object(SongService, 'create_song', side_effect=BusinessLogicValidationError(field="", message=""))

    response = client.post("/songs", json=song_request_schema.dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_update_song(mocker, client, song_request_schema, song_model):

    mocker.patch.object(SongApiMapper, 'map_to_song_model', return_value=song_model)
    mocker.patch.object(SongService, 'update_song', return_value=song_model)

    song_id = 1
    response = client.put(f"/songs/{song_id}", json=song_request_schema.dict())

    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.asyncio
async def test_update_song_bad_request(mocker, client, song_request_schema):
    
    mocker.patch.object(SongApiMapper, 'map_to_song_model', return_value=None)
    mocker.patch.object(SongService, 'update_song', side_effect=BusinessLogicValidationError(field="", message=""))

    song_id = 1
    response = client.put(f"/songs/{song_id}", json=song_request_schema.dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_update_song_not_found(mocker, client, song_request_schema):
        
    mocker.patch.object(SongApiMapper, 'map_to_song_model', return_value=None)
    mocker.patch.object(SongService, 'update_song', side_effect=NotFoundError)

    song_id = 1
    response = client.put(f"/songs/{song_id}", json=song_request_schema.dict())

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_song(mocker, client):
    
    mocker.patch.object(SongService, 'delete_song', return_value=None)

    song_id = 1
    response = client.delete(f"/songs/{song_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_song_not_found(mocker, client):
        
    mocker.patch.object(SongService, 'delete_song', side_effect=NotFoundError)

    song_id = 1
    response = client.delete(f"/songs/{song_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

