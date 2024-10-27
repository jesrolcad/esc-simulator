from datetime import datetime, timedelta
import pytest
from sqlalchemy import insert, select
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
        session.execute(insert(CeremonyEntity).values(id=1, ceremony_type_id=1, event_id=1, date=test_cases.sf1_date))

        session.execute(insert(SongCeremony).values(id=1, song_id=1, ceremony_id=1))
        session.execute(insert(SongCeremony).values(id=2, song_id=2, ceremony_id=1))

        session.execute(insert(VotingTypeEntity).values(id=1, name="JURY"))
        session.execute(insert(VotingEntity).values(id=1, country_id=1, song_id=2, ceremony_id=1, voting_type_id=1, score=10))

@pytest.fixture
def event():
    with get_db_as_context_manager() as session:
        session.execute(insert(EventEntity).values(id=1, year=2021, slogan="SLOGAN", host_city="HOST_CITY", arena="ARENA"))

@pytest.fixture
def ceremony_types():
    with get_db_as_context_manager() as session:
        session.execute(insert(CeremonyTypeEntity).values(id=1, name="SEMIFINAL 1", code="SF1"))
        session.execute(insert(CeremonyTypeEntity).values(id=2, name="SEMIFINAL 2", code="SF2"))
        session.execute(insert(CeremonyTypeEntity).values(id=3, name="GRAND FINAL", code="GF"))

@pytest.mark.parametrize("test_case", test_cases.get_events_test_cases)
def test_get_events(request, client, test_case):

    if test_case['case'] != "empty_list":
        request.getfixturevalue("events")

    
    response = client.get("/events")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == test_case['expected_event_count']
    assert response.json() == test_case['expected_response']

@pytest.mark.usefixtures("events")
def test_events_query(client):

    query = '''
        query {
            events {
                id
                year
                hostCity
                arena
                slogan
                ceremonies {
                    id
                    date
                    ceremonyType {
                        id
                        name
                        code
                    }
                }
            }
        }
        '''
    
    response = client.post("/graphql", json={"query": query})

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()['data']['events']
    assert len(response_data) == 1

    assert response_data[0] == test_cases.expected_event_query_response



@pytest.mark.usefixtures("events")
def test_get_event(client):

    response = client.get("/events/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_cases.expected_get_events_response

@pytest.mark.usefixtures("events")
def test_event_query(client):
    
    query = '''
        query {
            event(eventId: 1) {
                id
                year
                hostCity
                arena
                slogan
                ceremonies {
                    id
                    date
                    ceremonyType {
                        id
                        name
                        code
                    }
                }
            }
        }
        '''
    
    response = client.post("/graphql", json={"query": query})

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()['data']['event']
    assert response_data == test_cases.expected_event_query_response


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

@pytest.mark.parametrize("test_case", test_cases.create_update_event_positive_test_cases)
@pytest.mark.usefixtures("ceremony_types")
def test_create_event_positive(client, test_case):

    response = client.post("/events", json=test_case)

    response_id = response.json()['data']['id']

    with get_db_as_context_manager() as session:
        created_event = session.scalars(select(EventEntity).where(EventEntity.id == response_id)).first()
        created_event_ceremonies = created_event.ceremonies

    
    sf1_ceremony = created_event_ceremonies[0]
    sf2_ceremony = created_event_ceremonies[1]
    gf_ceremony = created_event_ceremonies[2]

    assert response.status_code == status.HTTP_201_CREATED
    assert created_event.year == test_case['year']
    assert created_event.slogan == test_case['slogan']
    assert created_event.host_city == test_case['host_city']
    assert created_event.arena == test_case['arena']
    assert len(created_event_ceremonies) == 3

    assert sf1_ceremony.ceremony_type_id == 1
    assert sf1_ceremony.date.strftime("%Y-%m-%d") == test_cases.sf1_date_str
    assert sf2_ceremony.ceremony_type_id == 2
    assert sf2_ceremony.date.strftime("%Y-%m-%d") == test_cases.sf2_date_str
    assert gf_ceremony.ceremony_type_id == 3
    assert gf_ceremony.date.strftime("%Y-%m-%d") == test_cases.grand_final_date_str

    for ceremony in created_event_ceremonies:
        assert ceremony.event_id == created_event.id

@pytest.mark.parametrize("test_case", test_cases.create_update_event_positive_test_cases)
@pytest.mark.usefixtures("ceremony_types")
def test_create_event_mutation_positive(client, test_case):

    query = f'''
    mutation {{
        createEvent(event: {{year: {test_case['year']}, slogan: "{test_case['slogan']}", 
        hostCity: "{test_case['host_city']}", arena: "{test_case['arena']}", grandFinalDate: "{test_case['grand_final_date']}"}}) {{
            id
        }}
    }}
    '''

    response = client.post("/graphql", json={"query": query})
    response_id = response.json()['data']['createEvent']['id']

    with get_db_as_context_manager() as session:
        created_event = session.scalars(select(EventEntity).where(EventEntity.id == response_id)).first()
        created_event_ceremonies = created_event.ceremonies

    sf1_ceremony = created_event_ceremonies[0]
    sf2_ceremony = created_event_ceremonies[1]
    gf_ceremony = created_event_ceremonies[2]

    assert created_event.year == test_case['year']
    assert created_event.slogan == test_case['slogan']
    assert created_event.host_city == test_case['host_city']
    assert created_event.arena == test_case['arena']
    assert len(created_event_ceremonies) == 3

    assert sf1_ceremony.ceremony_type_id == 1
    assert sf1_ceremony.date.strftime("%Y-%m-%d") == test_cases.sf1_date_str
    assert sf2_ceremony.ceremony_type_id == 2
    assert sf2_ceremony.date.strftime("%Y-%m-%d") == test_cases.sf2_date_str
    assert gf_ceremony.ceremony_type_id == 3
    assert gf_ceremony.date.strftime("%Y-%m-%d") == test_cases.grand_final_date_str

    for ceremony in created_event_ceremonies:
        assert ceremony.event_id == created_event.id
    
@pytest.mark.parametrize("test_case", test_cases.create_event_negative_test_cases)
def test_create_event_negative(client, test_case):

    response = client.post("/events", json=test_case['body'])

    response_errors = response.json()['errors']
    response_invalid_fields = [response_error['field'] for response_error in response_errors]

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_invalid_fields == test_case['invalid_fields']

@pytest.mark.parametrize("test_case", test_cases.create_event_mutation_negative_test_cases)
def test_create_event_mutation_negative(client, test_case):
    
    query = f'''
    mutation {{
        createEvent(event: {{year: {test_case['year']}, slogan: "{test_case['slogan']}", 
        hostCity: "{test_case['host_city']}", arena: "{test_case['arena']}", grandFinalDate: "{test_case['grand_final_date']}"}}) {{
            id
        }}
    }}
    '''

    response = client.post("/graphql", json={"query": query})
    assert response.json()['errors'] is not None


@pytest.mark.parametrize("test_case", test_cases.create_update_event_positive_test_cases)
@pytest.mark.usefixtures("event")
def test_update_event_positive(client, test_case):
    
    response = client.put("/events/1", json=test_case)

    with get_db_as_context_manager() as session:
        updated_event = session.scalars(select(EventEntity).where(EventEntity.id == 1)).first()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert updated_event.slogan == test_case['slogan']
    assert updated_event.host_city == test_case['host_city']
    assert updated_event.arena == test_case['arena']

@pytest.mark.parametrize("test_case", test_cases.create_update_event_positive_test_cases)
@pytest.mark.usefixtures("event")
def test_update_event_mutation_positive(client, test_case):
    
    query = f'''
    mutation {{
        updateEvent(eventId: 1, event: {{slogan: "{test_case['slogan']}", 
        hostCity: "{test_case['host_city']}", arena: "{test_case['arena']}"}}) {{
            success
        }}
    }}
    '''

    client.post("/graphql", json={"query": query})

    with get_db_as_context_manager() as session:
        updated_event = session.scalars(select(EventEntity).where(EventEntity.id == 1)).first()

    assert updated_event.slogan == test_case['slogan']
    assert updated_event.host_city == test_case['host_city']
    assert updated_event.arena == test_case['arena']


@pytest.mark.parametrize("test_case", test_cases.update_event_negative_test_cases)
@pytest.mark.usefixtures("event")
def test_update_event_negative(client, test_case):

    response = client.put("/events/1", json=test_case['body'])

    response_errors = response.json()['errors']
    response_invalid_fields = [response_error['field'] for response_error in response_errors]

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_invalid_fields == test_case['invalid_fields']

@pytest.mark.parametrize("test_case", test_cases.update_event_mutation_negative_test_cases)
@pytest.mark.usefixtures("event")
def test_update_event_mutation_negative(client, test_case):

    query = f'''
    mutation {{
        updateEvent(eventId: 1, event: {{slogan: "{test_case['slogan']}", 
        hostCity: "{test_case['host_city']}", arena: "{test_case['arena']}"}}) {{
            success
        }}
    }}
    '''

    response = client.post("/graphql", json={"query": query})
    assert response.json()['errors'] is not None


def test_update_event_not_found(client):

    event_id = 300

    response = client.put(f"/events/{event_id}", json=test_cases.create_update_event_positive_test_cases[0])

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.usefixtures("event")
def test_delete_event(client, event):

    response = client.delete("/events/1")

    with get_db_as_context_manager() as session:
        event = session.scalars(select(EventEntity).where(EventEntity.id == 1)).first()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert event is None

@pytest.mark.usefixtures("event")
def test_delete_event_mutation(client, event):
    
    query = '''
    mutation {
        deleteEvent(eventId: 1) {
            success
        }
    }
    '''

    client.post("/graphql", json={"query": query})

    with get_db_as_context_manager() as session:
        event = session.scalars(select(EventEntity).where(EventEntity.id == 1)).first()

    assert event is None

def test_delete_event_not_found(client):

    event_id = 300

    response = client.delete(f"/events/{event_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.usefixtures("events")
def test_delete_simulated_event(client):

    event_id = 1

    response = client.delete(f"/events/{event_id}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


    




