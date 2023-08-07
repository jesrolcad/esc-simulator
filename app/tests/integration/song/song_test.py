import pytest
from sqlalchemy import insert
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
        
@pytest.mark.usefixtures("song")
def test_get_song(client):

    song_id = 1

    Song.update_forward_refs()
    expected_country = Country(id=1, name="TEST", code="TEST")
    expected_event = Event(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST")
    expected_song = Song(id=1, title="TEST", artist="TEST", country=expected_country, event=expected_event,
                        belongs_to_host_country=False, jury_potential_score=10, televote_potential_score=10)

    response = client.get(f"/songs/{song_id}")
    
    song_response = Song.parse_obj(response.json())

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

    


