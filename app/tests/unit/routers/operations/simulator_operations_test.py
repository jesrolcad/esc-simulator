import pytest
import strawberry
from app.logic.models import CeremonyType, Participant, ParticipantResult, SimulationCeremonyResult
from app.logic.services.simulator_service import SimulatorService
from app.main import CustomContext

from app.routers.operations.simulation_operations import ParticipantDataResponseQL, ParticipantResultDataResponseQL, SimulationCeremonyResultResponseQL, SimulatorMutation, SimulatorQuery
from app.routers.schemas.simulator_schemas import ParticipantResultDataResponse


@pytest.fixture
def schema():
    return strawberry.Schema(query=SimulatorQuery, mutation=SimulatorMutation)

@pytest.fixture
def context(mocker):
    return CustomContext(db=mocker.Mock())

@pytest.fixture
def participant_model():
    return Participant(country_id=1, song_id=1, participant_info='Spain. Massiel - La, la, la. Jury potential score: 10 | Televote potential score: 10')

@pytest.fixture
def participant_ql_schema():
    return ParticipantDataResponseQL(country_id=1, song_id=1, participant_info='Spain. Massiel - La, la, la. Jury potential score: 10 | Televote potential score: 10')

@pytest.fixture
def simulation_ceremony_result_model():
    participant_result = ParticipantResult(country_id=1, song_id=1, participant_info='Spain. Massiel - La, la, la. Jury potential score: 10 | Televote potential score: 10', total_score=20, jury_score=10, televote_score=10)
    return SimulationCeremonyResult(ceremony_id=1, ceremony_type=CeremonyType(id=1, name='Test type', code='CT'), results=[participant_result])

@pytest.fixture
def simulation_ceremony_result_ql_schema():
    participant_result_ql_schema = ParticipantResultDataResponseQL(country_id=1, song_id=1, participant_info='Spain. Massiel - La, la, la. Jury potential score: 10 | Televote potential score: 10', position=1, total_score=20, jury_score=10, televote_score=10)
    return SimulationCeremonyResultResponseQL(ceremony_id=1, ceremony_type_id=1, ceremony_type_name='Test type', results=[participant_result_ql_schema])

def test_event_ceremony_participants_query(mocker, schema, context, participant_model, participant_ql_schema):
    mocker.patch.object(SimulatorService, 'get_simulation_participants_by_event_ceremony', return_value=[participant_model])
    mocker.patch.object(ParticipantDataResponseQL, 'map_to_participant_data_response_ql', return_value=participant_ql_schema)

    query = '''
    query {
        eventCeremonyParticipants(eventId: 1, ceremonyId: 1) {
            countryId
            songId
            participantInfo
        }
    }
    '''

    result = schema.execute_sync(query, context_value=context)
    assert not result.errors



def test_event_results_query(mocker, schema, context, simulation_ceremony_result_model, simulation_ceremony_result_ql_schema):
    mocker.patch.object(SimulatorService, 'get_simulation_event_results', return_value=[simulation_ceremony_result_model])
    mocker.patch.object(SimulationCeremonyResultResponseQL, 'map_to_simulation_ceremony_result_data_response_ql', return_value=simulation_ceremony_result_ql_schema)

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

    result = schema.execute_sync(query, context_value=context)
    assert not result.errors


def test_event_ceremony_type_results(mocker, schema, context, simulation_ceremony_result_model, simulation_ceremony_result_ql_schema):
    mocker.patch.object(SimulatorService, 'get_simulation_event_results_by_ceremony_type', return_value=simulation_ceremony_result_model)
    mocker.patch.object(SimulationCeremonyResultResponseQL, 'map_to_simulation_ceremony_result_data_response_ql', return_value=simulation_ceremony_result_ql_schema)

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

    result = schema.execute_sync(query, context_value=context)
    assert not result.errors

def test_create_event_simulation_mutation(mocker, schema, context):

    mocker.patch.object(SimulatorService, 'create_simulation')

    query = '''
    mutation {
        createEventSimulation(eventId: 1) {
            success
            message
        }
    }
    '''

    result = schema.execute_sync(query, context_value=context)
    assert not result.errors

def test_delete_event_simulation_mutation(mocker, schema, context):

    mocker.patch.object(SimulatorService, 'delete_simulation_by_event_id')

    query = '''
    mutation {
        deleteEventSimulation(eventId: 1) {
            success
            message
        }
    }
    '''

    result = schema.execute_sync(query, context_value=context)
    assert not result.errors

