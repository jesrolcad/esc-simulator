import pytest
from sqlalchemy import insert, select
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db_as_context_manager
from app.persistence.entities import CountryEntity, EventEntity, SongEntity
from app.logic.models import Song, Country, Event
from app.tests.integration.song import test_cases

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def song():
    with get_db_as_context_manager() as session:
        session.execute(insert(CountryEntity).values(id=1, name="TEST", code="TEST"))
        session.execute(insert(EventEntity).values(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST"))
        session.execute(insert(SongEntity).values(id=1, title="TEST", artist="TEST", country_id=1, event_id=1,
                                                belongs_to_host_country=False, jury_potential_score=10,
                                                televote_potential_score=10))

@pytest.fixture
def songs():
    with get_db_as_context_manager() as session:

        session.execute(insert(CountryEntity).values(id=1, name="TEST", code="TEST"))
        session.execute(insert(EventEntity).values(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST"))
        session.execute(insert(SongEntity).values(id=1, title="TEST", artist="TEST", country_id=1, event_id=1,
                                                belongs_to_host_country=False, jury_potential_score=10,
                                                televote_potential_score=10))
        
        session.execute(insert(CountryEntity).values(id=2, name="ABC", code="ABC"))
        session.execute(insert(EventEntity).values(id=2, year=2, slogan="ABC", host_city="ABC", arena="ABC"))
        session.execute(insert(SongEntity).values(id=2, title="ABC", artist="TEST2", country_id=2, event_id=2,
                                                belongs_to_host_country=False, jury_potential_score=10,
                                                televote_potential_score=10))
        
@pytest.fixture
def countries():
    with get_db_as_context_manager() as session:
        session.execute(insert(CountryEntity).values(id=1, name="TEST", code="TEST"))
        session.execute(insert(CountryEntity).values(id=2, name="ABC", code="ABC"))

@pytest.fixture
def events():
    with get_db_as_context_manager() as session:
        session.execute(insert(EventEntity).values(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST"))
        session.execute(insert(EventEntity).values(id=2, year=2, slogan="ABC", host_city="ABC", arena="ABC"))

@pytest.fixture
def setup_for_create_song_negative():

    with get_db_as_context_manager() as session:
        session.execute(insert(CountryEntity).values(id=1, name="TEST", code="TEST"))
        session.execute(insert(CountryEntity).values(id=2, name="ABC", code="ABC"))
        session.execute(insert(EventEntity).values(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST"))
        session.execute(insert(SongEntity).values(id=1, title="TEST", artist="TEST", country_id=1, event_id=1,
                                                belongs_to_host_country=True, jury_potential_score=10,
                                                televote_potential_score=10))
        
@pytest.fixture
def setup_for_update_song_negative():
    
    with get_db_as_context_manager() as session:
        session.execute(insert(CountryEntity).values(id=1, name="TEST", code="TEST"))
        session.execute(insert(CountryEntity).values(id=2, name="ABC", code="ABC"))
        session.execute(insert(EventEntity).values(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST"))
        session.execute(insert(EventEntity).values(id=2, year=2, slogan="ABC", host_city="ABC", arena="ABC"))
        session.execute(insert(SongEntity).values(id=1, title="TEST", artist="TEST", country_id=1, event_id=1,
                                                belongs_to_host_country=False, jury_potential_score=10,
                                                televote_potential_score=10))
        session.execute(insert(SongEntity).values(id=2, title="ABC", artist="TEST2", country_id=2, event_id=2,
                                                belongs_to_host_country=True, jury_potential_score=10,
                                                televote_potential_score=10))
        
@pytest.mark.usefixtures("song")
def test_get_song(client):

    song_id = 1

    Song.model_rebuild()
    expected_country = Country(id=1, name="TEST", code="TEST")
    expected_event = Event(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST")
    expected_song = Song(id=1, title="TEST", artist="TEST", country=expected_country, event=expected_event,
                        belongs_to_host_country=False, jury_potential_score=10, televote_potential_score=10)

    response = client.get(f"/songs/{song_id}")
    
    song_response = Song.model_validate(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert song_response.id == expected_song.id
    assert song_response.title == expected_song.title
    assert song_response.artist == expected_song.artist
    assert song_response.country == expected_song.country
    assert song_response.belongs_to_host_country == expected_song.belongs_to_host_country
    assert song_response.jury_potential_score == expected_song.jury_potential_score
    assert song_response.televote_potential_score == expected_song.televote_potential_score
    assert song_response.ceremonies == expected_song.ceremonies
    assert song_response.votings == expected_song.votings


def test_get_song_not_found(client):

    song_id = 1

    response = client.get(f"/songs/{song_id}")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.parametrize("test_case", test_cases.get_songs_test_cases)
def test_get_songs(request, client, test_case):

    if test_case['case'] != "empty_list":
        request.getfixturevalue("songs")

    response = client.get(f"/songs{test_case['filter']}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == test_case['expected_songs_count']

@pytest.mark.usefixtures("countries", "events")
@pytest.mark.parametrize("test_case", test_cases.create_update_song_positive_test_cases)
def test_create_song_positive(client, test_case):

    response = client.post("/songs", json=test_case)

    response_id = response.json()['data']['id']

    with get_db_as_context_manager() as session:
        created_song = session.scalars(select(SongEntity).where(SongEntity.id == response_id)).first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_id is not None
    assert created_song.title == test_case['title']
    assert created_song.artist == test_case['artist']
    assert created_song.country_id == test_case['country_id']
    assert created_song.event_id == test_case['event_id']
    assert created_song.belongs_to_host_country == test_case['belongs_to_host_country']
    assert created_song.jury_potential_score == test_case['jury_potential_score']
    assert created_song.televote_potential_score == test_case['televote_potential_score']

@pytest.mark.usefixtures("setup_for_create_song_negative")
@pytest.mark.parametrize("test_case", test_cases.create_update_song_negative_test_cases)
def test_create_song_negative(client, test_case):

    if test_case['case'] != "update_another_song_belongs_to_host_country":

        response = client.post("/songs", json=test_case['body'])

        response_errors = response.json()['errors']
        response_invalid_fields = [response_error['field'] for response_error in response_errors]

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_invalid_fields == test_case['invalid_fields']

@pytest.mark.usefixtures("song")
@pytest.mark.parametrize("test_case", test_cases.create_update_song_positive_test_cases)
def test_update_song_positive(client, test_case):
    
    song_id = 1

    response = client.put(f"/songs/{song_id}", json=test_case)

    with get_db_as_context_manager() as session:
        updated_song = session.scalars(select(SongEntity).where(SongEntity.id == song_id)).first()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert updated_song.title == test_case['title']
    assert updated_song.artist == test_case['artist']
    assert updated_song.country_id == test_case['country_id']
    assert updated_song.event_id == test_case['event_id']
    assert updated_song.belongs_to_host_country == test_case['belongs_to_host_country']
    assert updated_song.jury_potential_score == test_case['jury_potential_score']
    assert updated_song.televote_potential_score == test_case['televote_potential_score']

@pytest.mark.usefixtures("setup_for_update_song_negative")
@pytest.mark.parametrize("test_case", test_cases.create_update_song_negative_test_cases)
def test_update_song_negative(client, test_case):

    if test_case['case'] != "create_another_song_belongs_to_host_country":
        song_id = 1

        if test_case['case'] == "existing_song_by_country_and_event":
            song_id = 2
        
        response = client.put(f"/songs/{song_id}", json=test_case['body'])

        response_errors = response.json()['errors']
        response_invalid_fields = [response_error['field'] for response_error in response_errors]


        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_invalid_fields == test_case['invalid_fields']


def test_update_song_not_found(client):

    song_id = 1

    response = client.put(f"/songs/{song_id}", json={"title": "TEST", "artist": "TEST", "country_id": 1, "event_id": 1,
                                                "belongs_to_host_country": False, "jury_potential_score": 10, "televote_potential_score": 10})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.usefixtures("song")
def test_delete_song(client):

    song_id = 1

    response = client.delete(f"/songs/{song_id}")

    with get_db_as_context_manager() as session:
        deleted_song = session.scalars(select(SongEntity).where(SongEntity.id == song_id)).first()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert deleted_song is None


def test_delete_song_not_found(client):

    song_id = 1

    response = client.delete(f"/songs/{song_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND





