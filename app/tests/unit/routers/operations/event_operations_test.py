from datetime import datetime
import pytest
import strawberry

from app.logic.models import Ceremony, CeremonyType, Event
from app.logic.services.ceremony_service import CeremonyService
from app.logic.services.event_service import EventService
from app.main import CustomContext
from app.routers.api_mappers.ceremony_api_mapper import CeremonyApiMapper
from app.routers.api_mappers.event_api_mapper import EventApiMapper
from app.routers.operations.event_operations import EventDataResponseQL, EventMutation, EventQuery
from app.routers.schemas.common_schemas import CeremonyTypeDataResponseQL, CeremonyWithoutEventDataResponseQL

@pytest.fixture
def schema():
    return strawberry.Schema(query=EventQuery, mutation=EventMutation)

@pytest.fixture
def context(mocker):
    return CustomContext(db=mocker.Mock())

@pytest.fixture
def event_model():
    return Event(id=1, year=datetime.now().year, slogan='Test slogan', host_city='Test city', arena='Test arena')

@pytest.fixture
def event_ql_schema():
    return EventDataResponseQL(id=1, year=datetime.now().year, slogan='Test slogan', host_city='Test city', arena='Test arena')

@pytest.fixture
def ceremony_model():
    return Ceremony(id=1, date=datetime.now() , ceremony_type=CeremonyType(id=1, name='Test type', code='CT'))

@pytest.fixture
def ceremony_ql_schema():
    return CeremonyWithoutEventDataResponseQL(id=1, date=datetime.now(), ceremony_type=CeremonyTypeDataResponseQL(id=1, name='Test type', code='CT'))


def test_events_query(mocker, schema, context, event_model, event_ql_schema, ceremony_model, ceremony_ql_schema):
    mocker.patch.object(EventService, 'get_events', return_value=event_model)
    mocker.patch.object(CeremonyService, 'get_ceremonies_with_ceremony_types_by_event_id', return_value=ceremony_model)
    mocker.patch.object(CeremonyApiMapper, 'map_to_ceremony_without_event_data_response_ql', return_value=ceremony_ql_schema)
    mocker.patch.object(EventDataResponseQL, 'map_to_event_data_response_ql', return_value=event_ql_schema)

    query = '''
    query {
        events {
            id
            year
            slogan
            hostCity
            arena
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

    result = schema.execute_sync(query, context_value=context)
    assert not result.errors

def test_event_query(mocker, schema, context, event_model, event_ql_schema, ceremony_model, ceremony_ql_schema):
    mocker.patch.object(EventService, 'get_event', return_value=event_model)
    mocker.patch.object(CeremonyService, 'get_ceremonies_with_ceremony_types_by_event_id', return_value=ceremony_model)
    mocker.patch.object(CeremonyApiMapper, 'map_to_ceremony_without_event_data_response_ql', return_value=ceremony_ql_schema)
    mocker.patch.object(EventDataResponseQL, 'map_to_event_data_response_ql', return_value=event_ql_schema)

    query = '''
    query {
        event(eventId: 1) {
            id
            year
            slogan
            hostCity
            arena
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

    result = schema.execute_sync(query, context_value=context)
    assert not result.errors

def test_create_event_mutation(mocker, schema, context, event_model, event_ql_schema):
    mocker.patch.object(EventService, 'create_event_and_associated_ceremonies', return_value=event_model)
    mocker.patch.object(EventDataResponseQL, 'map_to_event_data_response_ql', return_value=event_ql_schema)

    grand_final_date = datetime.now().strftime('%Y-%m-%d')
    year = datetime.now().year

    mutation = f'''
    mutation {{
        createEvent(event: {{year: {year}, slogan: "Test slogan", hostCity: "Test city", arena: "Test arena", grandFinalDate: "{grand_final_date}"}}) {{
            id
            year
            slogan
            hostCity
            arena
        }}
    }}
    '''

    result = schema.execute_sync(mutation, context_value=context)
    assert not result.errors


def test_update_event_mutation(mocker, schema, context, event_model):
    mocker.patch.object(EventApiMapper, 'map_event_request_ql_to_event_model', return_value=event_model)
    mocker.patch.object(EventService, 'update_event')
    mocker.patch.object(EventDataResponseQL, 'map_to_event_data_response_ql')

    mutation = '''
    mutation {
        updateEvent(eventId: 1, event: {slogan: "Test slogan", hostCity: "Test city", arena: "Test arena"}) {
            success
            message
        }
    }
    '''

    result = schema.execute_sync(mutation, context_value=context)
    assert not result.errors

def test_delete_event_mutation(mocker, schema, context):
    mocker.patch.object(EventService, 'delete_event')
    
    mutation = '''
    mutation {
        deleteEvent(eventId: 1) {
            success
            message
        }
    }
    '''

    result = schema.execute_sync(mutation, context_value=context)
    assert not result.errors