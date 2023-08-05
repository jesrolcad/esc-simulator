import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.logic.services.country_service import CountryService
from app.routers.api_mappers.country_api_mapper import CountryApiMapper
from app.routers.schemas.country_schemas import CountryDataResponse
from app.logic.models import Country
from app.utils.exceptions import NotFoundError, AlreadyExistsError
from app.routers.schemas.api_schemas import ResultResponse
from app.routers.schemas.base_schemas import BaseId


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()

@pytest.fixture
def country_schema():
    return CountryDataResponse(id=1, name="TEST", code="TEST")

@pytest.fixture
def country_model():
    return Country(id=1, name="TEST", code="TEST")


@pytest.mark.asyncio
async def test_get_country(mocker, client, country_model, country_schema):

    mocker.patch.object(CountryService, "get_country", return_value=country_model)
    mocker.patch.object(CountryApiMapper, "map_to_country_data_response", return_value=country_schema)

    country_id = 1
    response = client.get(f"/countries/{country_id}")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_country_not_found(mocker, client):
    
    mocker.patch.object(CountryService, "get_country", side_effect=NotFoundError)

    country_id = 1
    response = client.get(f"/countries/{country_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_countries(mocker, client, country_model, country_schema):

    mocker.patch.object(CountryService, "get_countries", return_value=[country_model])
    mocker.patch.object(CountryApiMapper, "map_to_country_data_response", return_value=country_schema)

    response = client.get("/countries")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [country_schema.__dict__]


@pytest.mark.asyncio
async def test_create_country(mocker, client, country_model):

    mocker.patch.object(CountryApiMapper, "map_to_country_model", return_value=country_model)
    mocker.patch.object(CountryService, "create_country", return_value=country_model)

    expected_result = ResultResponse(message="Country created successfully", data=BaseId(id=country_model.id))

    response = client.post("/countries", json=country_model.__dict__)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_result.__dict__


@pytest.mark.asyncio
async def test_create_already_existing_country(mocker, client, country_model):

    mocker.patch.object(CountryApiMapper, "map_to_country_model", return_value=country_model)
    mocker.patch.object(CountryService, "create_country", side_effect=AlreadyExistsError)

    response = client.post("/countries", json=country_model.__dict__)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_update_country(mocker, client, country_model):

    mocker.patch.object(CountryApiMapper, "map_to_country_model", return_value=country_model)
    mocker.patch.object(CountryService, "update_country", return_value=None)

    country_id = 1
    response = client.put(f"/countries/{country_id}", json=country_model.__dict__)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_update_not_found_country(mocker, client, country_model):

    mocker.patch.object(CountryApiMapper, "map_to_country_model", return_value=country_model)
    mocker.patch.object(CountryService, "update_country", side_effect=NotFoundError)

    country_id = 1
    response = client.put(f"/countries/{country_id}", json=country_model.__dict__)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_already_existing_country_by_name_or_code(mocker, client, country_model):
    
    mocker.patch.object(CountryApiMapper, "map_to_country_model", return_value=country_model)
    mocker.patch.object(CountryService, "update_country", side_effect=AlreadyExistsError)

    country_id = 1
    response = client.put(f"/countries/{country_id}", json=country_model.__dict__)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_delete_country(mocker, client):

    mocker.patch.object(CountryService, "delete_country", return_value=None)

    country_id = 1
    response = client.delete(f"/countries/{country_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_not_found_country(mocker, client):
    
    mocker.patch.object(CountryService, "delete_country", side_effect=NotFoundError)

    country_id = 1
    response = client.delete(f"/countries/{country_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND