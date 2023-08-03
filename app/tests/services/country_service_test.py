import pytest
from app.logic.services.country_service import CountryService
from app.persistence.repositories.country_repository import CountryRepository
from app.logic.model_mappers import CountryModelMapper
from app.logic.models import Country
from app.persistence.entities import CountryEntity
from app.utils.exceptions import NotFoundError


@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()

@pytest.fixture
def country_entity():
    return CountryEntity(id=1, name="test", code="COD", songs=[], votings=[])

@pytest.fixture
def country_model():
    Country.update_forward_refs()
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
