import pytest
from sqlalchemy import insert, select
from fastapi import status
from fastapi.testclient import TestClient
from app.db.database import get_db_as_context_manager
from app.persistence.entities import CountryEntity, EventEntity, SongEntity
from app.main import app
from app.logic.models import Country, Song
from app.tests.integration.country import test_cases

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def country():
    with get_db_as_context_manager() as session:
        session.execute(insert(CountryEntity).values(id=1, name="TEST", code="TEST"))
        session.execute(insert(EventEntity).values(id=1, year=1, slogan="TEST", host_city="TEST", arena="TEST"))
        session.execute(insert(SongEntity).values(id=1, title="TEST", artist="TEST", country_id=1, event_id=1,
                                                belongs_to_host_country=False, jury_potential_score=10,
                                                televote_potential_score=10))

@pytest.fixture
def country_without_relations():
    with get_db_as_context_manager() as session:
        session.execute(insert(CountryEntity).values(id=1, name="TEST", code="TEST"))

@pytest.mark.usefixtures("country")
def test_get_country(client):

    expected_country = Country(id=1, name="TEST", code="TEST")
    country_id = 1

    response = client.get(f"/countries/{country_id}")

    country_response = Country.model_validate(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert country_response.id == expected_country.id
    assert country_response.name == expected_country.name
    assert country_response.code == expected_country.code


@pytest.mark.usefixtures("country")
def test_country_query(client):
    expected_country = Country(id=1, name="TEST", code="TEST")
    expected_song = Song(id=1, title="TEST", artist="TEST", belongs_to_host_country=False, jury_potential_score=10, televote_potential_score=10)

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

    response = client.post("/graphql", json={"query": query})

    country_response = response.json()['data']['country']

    assert country_response['id'] == expected_country.id
    assert country_response['name'] == expected_country.name
    assert country_response['code'] == expected_country.code
    assert len(country_response['songs']) == 1
    assert country_response['songs'][0]['id'] == expected_song.id
    assert country_response['songs'][0]['title'] == expected_song.title
    assert country_response['songs'][0]['artist'] == expected_song.artist
    assert country_response['songs'][0]['belongsToHostCountry'] == expected_song.belongs_to_host_country
    assert country_response['songs'][0]['juryPotentialScore'] == expected_song.jury_potential_score
    assert country_response['songs'][0]['televotePotentialScore'] == expected_song.televote_potential_score


def test_get_country_not_found(client):

    country_id = 1

    response = client.get(f"/countries/{country_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.parametrize("test_case", test_cases.get_countries_test_cases)
def test_get_countries(request, client, test_case):

    if test_case['case'] == "not_empty_list":
        request.getfixturevalue("country")

    response = client.get("/countries")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == test_case['expected_countries_count']

@pytest.mark.usefixtures("country")
def test_countries_query(client):
    expected_country = Country(id=1, name="TEST", code="TEST")
    expected_song = Song(id=1, title="TEST", artist="TEST", belongs_to_host_country=False, jury_potential_score=10, televote_potential_score=10)
    
    query = '''
        query {
            countries {
                id
                name
                code
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

    response = client.post("/graphql", json={"query": query})

    assert len(response.json()['data']['countries']) == 1
    country_response = response.json()['data']['countries'][0]
    assert country_response['id'] == expected_country.id
    assert country_response['name'] == expected_country.name
    assert country_response['code'] == expected_country.code
    assert len(country_response['songs']) == 1
    assert country_response['songs'][0]['id'] == expected_song.id
    assert country_response['songs'][0]['title'] == expected_song.title
    assert country_response['songs'][0]['artist'] == expected_song.artist
    assert country_response['songs'][0]['belongsToHostCountry'] == expected_song.belongs_to_host_country
    assert country_response['songs'][0]['juryPotentialScore'] == expected_song.jury_potential_score
    assert country_response['songs'][0]['televotePotentialScore'] == expected_song.televote_potential_score


@pytest.mark.parametrize("test_case", test_cases.create_update_country_positive_test_cases)
def test_create_country_positive(client, test_case):

    response = client.post("/countries", json=test_case)

    response_id = response.json()['data']['id']
    
    with get_db_as_context_manager() as session:
        created_country = session.scalars(select(CountryEntity).where(CountryEntity.id == response_id)).first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_id is not None
    assert created_country.name == test_case['name']
    assert created_country.code == test_case['code']

@pytest.mark.parametrize("test_case", test_cases.create_update_country_positive_test_cases)
def test_create_country_mutation_positive(client, test_case):

    query = f'''
        mutation {{
            createCountry(country: {{name: "{test_case['name']}", code: "{test_case['code']}"}}) {{
                id
            }}
        }}
    '''

    response = client.post("/graphql", json={"query": query})

    response_country = response.json()['data']['createCountry']

    with get_db_as_context_manager() as session:
        created_country = session.scalars(select(CountryEntity).where(CountryEntity.id == response_country['id'])).first()

    assert response_country['id'] is not None
    assert created_country.name == test_case['name']
    assert created_country.code == test_case['code']


@pytest.mark.usefixtures("country")
@pytest.mark.parametrize("test_case", test_cases.create_update_country_negative_test_cases)
def test_create_country_negative(client, test_case):

    response = client.post("/countries", json=test_case['body'])

    response_errors = response.json()['errors']
    response_invalid_fields = [response_error['field'] for response_error in response_errors]

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_invalid_fields == test_case['invalid_fields']

@pytest.mark.parametrize("test_case", test_cases.create_update_country_mutation_negative_test_cases)
def test_create_country_mutation_negative(client, test_case):

    query = f'''
        mutation {{
            createCountry(country: {{name: "{test_case['name']}", code: "{test_case['code']}"}}) {{
                id
            }}
        }}
    '''

    response = client.post("/graphql", json={"query": query})

    assert response.json()['errors'] is not None

@pytest.mark.usefixtures("country")
@pytest.mark.parametrize("test_case", test_cases.create_update_country_positive_test_cases)
def test_update_country_positive(client, test_case):

    country_id = 1
    response = client.put(f"/countries/{country_id}", json=test_case)

    with get_db_as_context_manager() as session:
        updated_country = session.scalars(select(CountryEntity).where(CountryEntity.id == country_id)).first()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert updated_country.name == test_case['name']
    assert updated_country.code == test_case['code']

@pytest.mark.usefixtures("country")
@pytest.mark.parametrize("test_case", test_cases.create_update_country_positive_test_cases)
def test_update_country_mutation_positive(client, test_case):

    country_id = 1
    query = f'''
        mutation {{
            updateCountry(countryId: {country_id}, country: {{name: "{test_case['name']}", code: "{test_case['code']}"}}) {{
                success
            }}
        }}
    '''

    client.post("/graphql", json={"query": query})

    with get_db_as_context_manager() as session:
        updated_country = session.scalars(select(CountryEntity).where(CountryEntity.id == country_id)).first()

    assert updated_country.name == test_case['name']
    assert updated_country.code == test_case['code']


@pytest.mark.parametrize("test_case", test_cases.create_update_country_negative_test_cases)
def test_update_country_negative(client, test_case):

    with get_db_as_context_manager() as session:
        session.execute(insert(CountryEntity).values(id=1, name="TEST", code="TEST"))
        session.execute(insert(CountryEntity).values(id=2, name="TEST2", code="TEST2"))

    country_id = 2
    response = client.put(f"/countries/{country_id}", json=test_case['body'])

    response_errors = response.json()['errors']
    response_invalid_fields = [response_error['field'] for response_error in response_errors]

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_invalid_fields == test_case['invalid_fields']

@pytest.mark.usefixtures("country")
@pytest.mark.parametrize("test_case", test_cases.create_update_country_mutation_negative_test_cases)
def test_update_country_mutation_negative(client, test_case):

    country_id = 1
    query = f'''
        mutation {{
            updateCountry(countryId: {country_id}, country: {{name: "{test_case['name']}", code: "{test_case['code']}"}}) {{
                success
            }}
        }}
    '''

    response = client.post("/graphql", json={"query": query})

    assert response.json()['errors'] is not None


def test_update_country_not_found(client):

    country_id = 1
    response = client.put(f"/countries/{country_id}", json={"name": "TEST", "code": "TEST"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.usefixtures("country_without_relations")
def test_delete_country_positive(client):

    country_id = 1

    response = client.delete(f"/countries/{country_id}")

    with get_db_as_context_manager() as session:
        deleted_country = session.scalars(select(CountryEntity).where(CountryEntity.id == country_id)).first()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert deleted_country is None

@pytest.mark.usefixtures("country_without_relations")
def test_delete_country_mutation_positive(client):

    country_id = 1

    query = f'''
        mutation {{
            deleteCountry(countryId: {country_id}) {{
                success
            }}
        }}
    '''

    client.post("/graphql", json={"query": query})

    with get_db_as_context_manager() as session:
        deleted_country = session.scalars(select(CountryEntity).where(CountryEntity.id == country_id)).first()

    assert deleted_country is None


def test_delete_country_not_found(client):
    
    country_id = 1

    response = client.delete(f"/countries/{country_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

