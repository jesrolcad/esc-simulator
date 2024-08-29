import pytest
from sqlalchemy import insert,select
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db_as_context_manager
from app.persistence.entities import CeremonyEntity, CeremonyTypeEntity, CountryEntity, EventEntity, SongCeremony, SongEntity, VotingEntity, VotingTypeEntity
from app.tests.integration.simulator import test_cases

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
                                                belongs_to_host_country=False, jury_potential_score=8,
                                                televote_potential_score=8))

        session.execute(insert(CeremonyTypeEntity).values(id=1, name="SEMIFINAL 1", code="SF1"))
        session.execute(insert(CeremonyTypeEntity).values(id=2, name="SEMIFINAL 2", code="SF2"))
        session.execute(insert(CeremonyTypeEntity).values(id=3, name="GRAND FINAL", code="GF"))


        session.execute(insert(CeremonyEntity).values(id=1, ceremony_type_id=1, event_id=1, date="2021-01-01"))
        session.execute(insert(CeremonyEntity).values(id=2, ceremony_type_id=2, event_id=1, date="2021-01-02"))
        session.execute(insert(CeremonyEntity).values(id=3, ceremony_type_id=3, event_id=1, date="2021-01-03"))

        session.execute(insert(VotingTypeEntity).values(id=1, name="Jury"))
        session.execute(insert(VotingTypeEntity).values(id=2, name="Televote"))

        session.execute(insert(VotingEntity).values(id=1, ceremony_id=1, country_id=1, song_id=2, voting_type_id=1, score=1))
        session.execute(insert(VotingEntity).values(id=2, ceremony_id=1, country_id=1, song_id=2, voting_type_id=2, score=12))

        session.execute(insert(VotingEntity).values(id=3, ceremony_id=1, country_id=2, song_id=1, voting_type_id=1, score=10))
        session.execute(insert(VotingEntity).values(id=4, ceremony_id=1, country_id=2, song_id=1, voting_type_id=2, score=6))

        session.execute(insert(SongCeremony).values(id=1, song_id=1, ceremony_id=1))




@pytest.mark.parametrize("test_case", test_cases.get_event_ceremony_participants_test_cases)
def test_get_event_ceremony_participants(request, client, test_case):

    if test_case['case'] != "empty_list":
        request.getfixturevalue("events")
    

    response = client.get("/simulator/events/1/ceremonies/1/participants")
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == test_case['expected_participant_count']
    assert response.json() == test_case["expected_response"]

@pytest.mark.parametrize("test_case", test_cases.get_event_results_test_cases)
def test_get_event_results(request, client, test_case):
    
    if test_case['case'] != "empty_list":
        request.getfixturevalue("events")

    response = client.get("/simulator/events/1")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == test_case['expected_ceremony_results_count']
    assert response.json() == test_case["expected_response"]


def test_get_event_ceremony_type_results(request, client):
    request.getfixturevalue("events")

    response = client.get("/simulator/events/1/ceremony-types/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_cases.get_event_ceremony_type_results_test_cases["expected_response"]

def test_get_event_ceremony_type_results_not_found(client):

    response = client.get("/simulator/events/1/ceremony-types/3")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    


