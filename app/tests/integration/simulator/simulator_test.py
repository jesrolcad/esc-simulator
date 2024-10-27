import random
import pytest
from sqlalchemy import func, insert,select
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

@pytest.fixture
def create_simulation_event_fixture():
    with get_db_as_context_manager() as session:
        session.execute(insert(EventEntity).values(id=1, year=1, slogan="EVENT", host_city="HOST_CITY", arena="ARENA"))

        session.execute(insert(CeremonyTypeEntity).values(id=1, name="SEMIFINAL 1", code="SF1"))
        session.execute(insert(CeremonyTypeEntity).values(id=2, name="SEMIFINAL 2", code="SF2"))
        session.execute(insert(CeremonyTypeEntity).values(id=3, name="GRAND FINAL", code="GF"))

        session.execute(insert(CeremonyEntity).values(id=1, ceremony_type_id=1, event_id=1, date="2021-01-01"))
        session.execute(insert(CeremonyEntity).values(id=2, ceremony_type_id=2, event_id=1, date="2021-01-02"))
        session.execute(insert(CeremonyEntity).values(id=3, ceremony_type_id=3, event_id=1, date="2021-01-03"))

        session.execute(insert(VotingTypeEntity).values(id=1, name="Jury"))
        session.execute(insert(VotingTypeEntity).values(id=2, name="Televote"))

        session.execute(insert(CountryEntity), build_simulation_countries())
        session.execute(insert(SongEntity), build_simulation_songs())


@pytest.mark.parametrize("test_case", test_cases.get_event_ceremony_participants_test_cases)
def test_get_event_ceremony_participants(request, client, test_case):

    if test_case['case'] != "empty_list":
        request.getfixturevalue("events")
    

    response = client.get("/simulator/events/1/ceremonies/1/participants")
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == test_case['expected_participant_count']
    assert response.json() == test_case["expected_response"]

@pytest.mark.usefixtures("events")
def test_event_ceremony_participants_query(client):

    query = '''
    query {
        eventCeremonyParticipants(eventId: 1, ceremonyId: 1) {
            countryId
            songId
            participantInfo
        }
    }
    '''

    response = client.post("/graphql", json={"query": query})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["eventCeremonyParticipants"] == test_cases.event_ceremony_participants_query_expected_response


@pytest.mark.parametrize("test_case", test_cases.get_event_results_test_cases)
def test_get_event_results(request, client, test_case):
    
    if test_case['case'] != "empty_list":
        request.getfixturevalue("events")

    response = client.get("/simulator/events/1")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == test_case['expected_ceremony_results_count']
    assert response.json() == test_case["expected_response"]

@pytest.mark.usefixtures("events")
def test_event_results_query(client):

    query = '''
    query {
        eventResults(eventId: 1) {
            ceremonyId
            ceremonyTypeId
            ceremonyTypeName
            results {
                countryId
                songId
                participantInfo
                position
                totalScore
                juryScore
                televoteScore
            }
        }
    }
    '''

    response = client.post("/graphql", json={"query": query})

    assert response.json()["data"]["eventResults"] == test_cases.event_results_query_expected_response

@pytest.mark.usefixtures("events")
def test_get_event_ceremony_type_results(client):

    response = client.get("/simulator/events/1/ceremony-types/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_cases.get_event_ceremony_type_results_test_cases["expected_response"]

@pytest.mark.usefixtures("events")
def test_event_ceremony_type_results_query(client):

    query = '''
    query {
        eventCeremonyTypeResults(eventId: 1, ceremonyTypeId: 1) {
            ceremonyId
            ceremonyTypeId
            ceremonyTypeName
            results {
                countryId
                songId
                participantInfo
                position
                totalScore
                juryScore
                televoteScore
            }
        }
    }
    '''

    response = client.post("/graphql", json={"query": query})

    assert response.json()["data"]["eventCeremonyTypeResults"] == test_cases.event_results_query_expected_response[0]

def test_get_event_ceremony_type_results_not_found(client):

    response = client.get("/simulator/events/1/ceremony-types/3")

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.usefixtures("create_simulation_event_fixture")
def test_create_simulation(client):

    response = client.post("/simulator/events/1/simulate")

    with get_db_as_context_manager() as session:
        votings_count = session.execute(select(func.count()).where(VotingEntity.ceremony_id.in_([1,2,3]))).scalar()
        song_ceremonies_count = session.execute(select(func.count()).where(SongCeremony.c.ceremony_id.in_([1,2,3]))).scalar()

    assert votings_count > 0
    assert song_ceremonies_count > 0
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.usefixtures("create_simulation_event_fixture")
def test_create_simulation_mutation(client):

    query = '''
    mutation {
        createEventSimulation(eventId: 1) {
            success
            message
        }
    }
    '''

    client.post("/graphql", json={"query": query})

    with get_db_as_context_manager() as session:
        votings_count = session.execute(select(func.count()).where(VotingEntity.ceremony_id.in_([1,2,3]))).scalar()
        song_ceremonies_count = session.execute(select(func.count()).where(SongCeremony.c.ceremony_id.in_([1,2,3]))).scalar()

    assert votings_count > 0
    assert song_ceremonies_count > 0

@pytest.mark.usefixtures("events")
def test_delete_event_simulation(client):

    response = client.delete("/simulator/events/1")

    with get_db_as_context_manager() as session:
        votings_count = session.execute(select(func.count()).where(VotingEntity.ceremony_id.in_([1,2,3]))).scalar()
        song_ceremonies_count = session.execute(select(func.count()).where(SongCeremony.c.ceremony_id.in_([1,2,3]))).scalar()

    assert votings_count == 0
    assert song_ceremonies_count == 0
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.usefixtures("events")
def test_delete_event_simulation_mutation(client):

    query = '''
    mutation {
        deleteEventSimulation(eventId: 1) {
            success
            message
        }
    }
    '''

    client.post("/graphql", json={"query": query})

    with get_db_as_context_manager() as session:
        votings_count = session.execute(select(func.count()).where(VotingEntity.ceremony_id.in_([1,2,3]))).scalar()
        song_ceremonies_count = session.execute(select(func.count()).where(SongCeremony.c.ceremony_id.in_([1,2,3]))).scalar()

    assert votings_count == 0
    assert song_ceremonies_count == 0

@pytest.mark.usefixtures("events")
def test_delete_event_simulation_not_found(client):

    response = client.delete("/simulator/events/1000")

    assert response.status_code == status.HTTP_404_NOT_FOUND

def build_simulation_countries()->list[dict]:

    return [{"id": i, "name": "Country" + str(i), "code": "CO" + str(i)} for i in range(1, 41)]


def build_simulation_songs()->list[dict]:

    belongs_to_host_country_song = {"id": 1, "country_id": 1, "event_id": 1, "title": "Song1", "artist": "Artist1", 
                                    "belongs_to_host_country": True, "jury_potential_score": random.randint(1,10), "televote_potential_score": random.randint(1,10)}

    rest_of_songs = [{"id": i, "country_id": i, "event_id": 1, "title": "Song" + str(i), "artist": "Artist" + str(i), 
                      "belongs_to_host_country": False, "jury_potential_score": random.randint(1,10), "televote_potential_score": random.randint(1,10)} 
                      for i in range(2, 41)]

    return [belongs_to_host_country_song] + rest_of_songs
    
    


