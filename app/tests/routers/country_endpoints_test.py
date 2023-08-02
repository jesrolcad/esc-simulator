import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.logic.services.country_service import CountryService
from app.routers.api_mappers.country_api_mapper import CountryApiMapper
from app.routers.schemas.country_schemas import CountryDataResponse
from app.logic.models import Country
from app.utils.exceptions import NotFoundError


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