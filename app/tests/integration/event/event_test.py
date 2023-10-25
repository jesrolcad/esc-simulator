import pytest
from sqlalchemy import insert
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db_as_context_manager
from app.persistence.entities import EventEntity, CountryEntity, SongEntity, CeremonyTypeEntity, CeremonyEntity, VotingTypeEntity, VotingEntity, SongCeremony
from app.tests.integration.event import test_cases


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def events():
    with get_db_as_context_manager() as session:
        session.execute(insert(CountryEntity).values(id=1, name="COUNTRY", code="COU"))
        session.execute(insert(CountryEntity).values(id=2, name="COUNTRY2", code="CO2"))
        session.execute(insert(EventEntity).values(id=1, year=1, slogan="EVENT", host_city="HOST_CITY", arena="ARENA"))
        session.execute(insert(SongEntity).values(id=1, title="SONG1", artist="SONG_ARTIST1", country_id=1, event_id=1,
                                                belongs_to_host_country=False, jury_potential_score=10,
                                                televote_potential_score=10))
        session.execute(insert(SongEntity).values(id=2, title="SONG2", artist="SONG_ARTIST2", country_id=2, event_id=1,
                                                belongs_to_host_country=True, jury_potential_score=10,
                                                televote_potential_score=10))
        session.execute(insert(CeremonyTypeEntity).values(id=1, name="SEMIFINAL 1", code="SF1"))
        session.execute(insert(CeremonyEntity).values(id=1, ceremony_type_id=1, event_id=1, date="2021-01-01"))

        session.execute(insert(SongCeremony).values(id=1, song_id=1, ceremony_id=1))
        session.execute(insert(SongCeremony).values(id=2, song_id=2, ceremony_id=1))

        session.execute(insert(VotingTypeEntity).values(id=1, name="JURY"))
        session.execute(insert(VotingEntity).values(id=1, country_id=1, song_id=2, ceremony_id=1, voting_type_id=1, score=10))


@pytest.mark.parametrize("test_case", test_cases.get_events_test_cases)
def test_get_events(request, client, test_case):

    if test_case['case'] != "empty_list":
        request.getfixturevalue("events")

    
    response = client.get("/events")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == test_case['expected_event_count']
    assert response.json() == test_case['expected_response']

@pytest.mark.usefixtures("events")
def test_get_event(client):

    response = client.get("/events/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_cases.expected_get_events_response


def test_get_event_not_found(client):

    response = client.get("/events/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.usefixtures("events")
def test_get_event_ceremony(client):

    response = client.get("/events/1/ceremonies/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_cases.expected_get_event_ceremony_response


def test_get_event_ceremony_not_found(client):

    response = client.get("/events/1/ceremonies/1000")

    assert response.status_code == status.HTTP_404_NOT_FOUND

