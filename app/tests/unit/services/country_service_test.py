import pytest
from app.logic.services.country_service import CountryService
from app.persistence.repositories.country_repository import CountryRepository
from app.logic.model_mappers import CountryModelMapper
from app.logic.models import Country
from app.persistence.entities import CountryEntity
from app.utils.exceptions import NotFoundError, AlreadyExistsError


@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()

@pytest.fixture
def country_entity():
    return CountryEntity(id=1, name="test", code="COD", songs=[], votings=[])

@pytest.fixture
def country_model():
    Country.model_rebuild()
    return Country(id=1, name="test", code="COD", songs=[], votings=[])

def test_get_country(mocker, mock_session, country_entity, country_model):

    mocker.patch.object(CountryRepository, "get_country", return_value=country_entity)
    mocker.patch.object(CountryModelMapper, "map_to_country_model", return_value=country_model)

    country_id = 1
    result = CountryService(mock_session).get_country(id=country_id)

    assert isinstance(result, Country)
    assert result == country_model


def test_get_country_not_found(mocker, mock_session):

    mocker.patch.object(CountryRepository, "get_country", return_value=None)

    country_id = 1

    with pytest.raises(NotFoundError) as exception:
        CountryService(mock_session).get_country(id=country_id)
        assert exception.field == "country_id"

def test_get_countries(mocker, mock_session, country_entity, country_model):

    mocker.patch.object(CountryRepository, "get_countries", return_value=[country_entity])
    mocker.patch.object(CountryModelMapper, "map_to_country_model", return_value=country_model)

    result = CountryService(mock_session).get_countries()

    assert isinstance(result, list)
    assert isinstance(result[0], Country)
    assert result[0] == country_model
    CountryRepository.get_countries.assert_called_once()

def test_create_country(mocker, mock_session, country_entity, country_model):

    mocker.patch.object(CountryRepository, "get_country_by_name_or_code", return_value=None)
    mocker.patch.object(CountryModelMapper, "map_to_country_entity", return_value=country_entity)
    mocker.patch.object(CountryRepository, "create_country", return_value=country_entity)
    mocker.patch.object(CountryModelMapper, "map_to_country_model", return_value=country_model)

    result = CountryService(mock_session).create_country(country_model)

    assert isinstance(result, Country)
    assert result == country_model

def test_create_already_existing_country(mocker, mock_session, country_entity, country_model):

    mocker.patch.object(CountryRepository, "get_country_by_name_or_code", return_value=country_entity)

    with pytest.raises(AlreadyExistsError) as exception:
        CountryService(mock_session).create_country(country_model)
        assert exception.field == "name,code"

def test_update_country(mocker, mock_session, country_entity, country_model):

    mocker.patch.object(CountryRepository, "get_country", return_value=country_entity)
    mocker.patch.object(CountryRepository, "get_country_by_name_or_code", return_value=None)
    mocker.patch.object(CountryModelMapper, "map_to_country_entity", return_value=country_entity)
    mocker.patch.object(CountryRepository, "update_country", return_value=None)

    country_id = 1

    try:
        CountryService(mock_session).update_country(country_id=country_id, country=country_model)

    except Exception as exception:
        pytest.fail(f"Test failed with exception: {exception}")


def test_update_not_found_country(mocker, mock_session, country_model):

    mocker.patch.object(CountryRepository, "get_country", return_value = None)

    country_id = 1

    with pytest.raises(NotFoundError) as exception:
        CountryService(mock_session).update_country(country_id=country_id, country=country_model)
        assert exception.field == "country_id"


def test_update_already_existing_country_by_name_or_code(mocker, mock_session, country_entity, country_model):

    mocker.patch.object(CountryRepository, "get_country", return_value=country_entity)
    mocker.patch.object(CountryRepository, "get_country_by_name_or_code", return_value=country_entity)

    country_id = 1

    with pytest.raises(AlreadyExistsError) as exception:
        CountryService(mock_session).update_country(country_id=country_id, country=country_model)
        assert exception.field == "name,code"

def test_delete_country(mocker, mock_session, country_entity):

    mocker.patch.object(CountryRepository, "get_country", return_value=country_entity)
    mocker.patch.object(CountryRepository, "delete_country", return_value=None)

    country_id = 1

    try:
        CountryService(mock_session).delete_country(country_id=country_id)
    except Exception as exception:
        pytest.fail(f"Test failed with exception: {exception}")

def test_delete_not_found_country(mocker, mock_session):

    mocker.patch.object(CountryRepository, "get_country", return_value=None)

    country_id = 1

    with pytest.raises(NotFoundError) as exception:
        CountryService(mock_session).delete_country(country_id=country_id)
        assert exception.field == "country_id"