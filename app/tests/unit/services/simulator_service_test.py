from ast import arg
import datetime
from distutils.command import build
import pytest
import random

from app.logic.models import Ceremony, CeremonyType, Country, Participant, Song, SimulationSong
from app.logic.services.simulator_service import SimulatorService
from app.logic.services.song_service import SongService
from app.logic.services.ceremony_service import CeremonyService
from app.persistence.entities import CeremonyEntity
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.model_mappers import CeremonyModelMapper, SimulationModelMapper
from app.persistence.repositories.voting_repository import VotingRepository
from app.utils.exceptions import NotFoundError
from app.utils import constants

@pytest.fixture
def mock_session(mocker):
    return mocker.Mock()

@pytest.fixture
def participant_model():
    return Participant(country_id=1, song_id=1, participant_info="Italy. Måneskin - Zitti e buoni. Jury potential score: 10 | Televote potential score: 9")


@pytest.fixture
def ceremony_entity():
    return CeremonyEntity(id=1, ceremony_type_id=1, event_id=1, date=datetime.datetime.now())

@pytest.fixture
def ceremony_model():
    country = Country(id=1, name="Italy", code="ITA")
    song = Song(id=1, title="Zitti e buoni", artist="Måneskin", jury_potential_score=10, televote_potential_score=9, belongs_to_host_country=False, country=country)
    return Ceremony(ceremony_type=CeremonyType(id=1, name="Semifinal 1", code="SF1"), songs=[song])

@pytest.fixture
def simulation_song_model():
    return SimulationSong(song_id=1, country_id=2, jury_potential_score=10, televote_potential_score=3)


def test_get_simulation_participants_by_event_ceremony(mocker, mock_session, ceremony_entity, ceremony_model, participant_model):

    mocker.patch.object(CeremonyRepository, 'get_event_ceremony', return_value=ceremony_entity)
    mocker.patch.object(CeremonyModelMapper,'map_to_ceremony_model_without_event', return_value=ceremony_model)
    mocker.patch.object(SimulationModelMapper, 'build_participant_info', return_value=participant_model)

    result = SimulatorService(mock_session).get_simulation_participants_by_event_ceremony(event_id=1, ceremony_id=1)

    assert isinstance(result, list)
    assert result[0] == participant_model

def test_get_simulation_event_results(mocker, mock_session):

    mocker.patch.object(VotingRepository, 'get_scores_by_event_id', return_value=[])
    mocker.patch.object(SimulationModelMapper,'map_to_simulation_ceremony_result_model_list', return_value=[])

    result = SimulatorService(mock_session).get_simulation_event_results(event_id=1)

    SimulationModelMapper().map_to_simulation_ceremony_result_model_list.assert_called_once()

    assert isinstance(result, list)
    assert not result

def test_get_simulation_event_results_empty(mocker, mock_session):

    mocker.patch.object(VotingRepository, 'get_scores_by_event_id', return_value=None)
    mocker.patch.object(SimulationModelMapper,'map_to_simulation_ceremony_result_model_list', return_value=[])

    result = SimulatorService(mock_session).get_simulation_event_results(event_id=1)

    SimulationModelMapper().map_to_simulation_ceremony_result_model_list.assert_not_called()

    assert isinstance(result, list)
    assert not result

@pytest.mark.parametrize("scores", [None, []])
def test_get_simulation_event_results_by_ceremony_type_none_empty(mocker, mock_session, scores):

    mocker.patch.object(VotingRepository, 'get_scores_by_event_id_and_ceremony_type_id', return_value=scores)
    
    with pytest.raises(Exception) as exception:
        SimulatorService(mock_session).get_simulation_event_results_by_ceremony_type(event_id=1, ceremony_type_id=1)
        assert exception.field == "event_id, ceremony_type_id"


def test_get_simulation_event_results_by_ceremony_type(mocker, mock_session):

    scores = [
        (1, 1, 1, 1, 1, 1),
        (2, 2, 2, 2, 2, 2)
    ]

    mocker.patch.object(VotingRepository, 'get_scores_by_event_id_and_ceremony_type_id', return_value=scores)
    mocker.patch.object(SimulationModelMapper,'map_to_simulation_ceremony_result_model', return_value=None)

    result = SimulatorService(mock_session).get_simulation_event_results_by_ceremony_type(event_id=1, ceremony_type_id=1)

    SimulationModelMapper().map_to_simulation_ceremony_result_model.assert_called_once()

    assert result is None

def test_create_simulation_no_simulation_songs_test(mocker, mock_session):

    event_id = 1

    mocker.patch.object(SongService,'get_simulation_songs_by_event_id', return_value=None)

    with pytest.raises(NotFoundError) as exception:
        SimulatorService(mock_session).create_simulation(event_id=event_id)
        assert exception.field == "event_id"
        assert exception.message == f"No songs found for event_id {event_id}"

def test_create_simulation_no_ceremonies_test(mocker, mock_session, simulation_song_model):

    event_id = 1

    mocker.patch.object(SongService,'get_simulation_songs_by_event_id', return_value=[simulation_song_model])
    mocker.patch.object(CeremonyService,'get_event_ceremonies', return_value=None)

    with pytest.raises(NotFoundError) as exception:
        SimulatorService(mock_session).create_simulation(event_id=event_id)
        assert exception.field == "event_id"
        assert exception.message == f"No ceremonies found for event_id {event_id}"

def test_create_simulation(mocker, mock_session):

    event_id = 1

    simulation_songs = build_simulation_songs(number_of_songs=35)

    automatic_qualifiers = simulation_songs[30:]

    event_ceremonies = {1:10, 2:11, 3:12}
    
    mocker.patch.object(SongService,'get_simulation_songs_by_event_id', return_value=simulation_songs)
    mocker.patch.object(CeremonyService,'get_event_ceremonies', return_value=event_ceremonies)

    # divide songs into semifinals
    mocker.patch.object(CeremonyService, 'add_songs_to_ceremony')

    # simulate ceremony 
    mocker.patch.object(SongService, 'get_simulation_songs_by_ceremony_id', side_effect=[simulation_songs[:15], simulation_songs[15:30], simulation_songs[:10] + simulation_songs[10:20] + automatic_qualifiers])
    mocker.patch.object(VotingRepository, 'add_votings')

    qualified_songs_for_grand_final = simulation_songs[:10] + simulation_songs[10:20]

    mocker.patch.object(VotingRepository, 'get_qualified_song_ids_for_grand_final', return_value = qualified_songs_for_grand_final)

    mocker.patch.object(SongService, 'get_automatic_qualified_songs_for_grand_final_by_event_id', return_value = automatic_qualifiers)
    
    try:
        SimulatorService(mock_session).create_simulation(event_id=event_id)
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

    


def test_divide_songs_into_semifinals(mocker, mock_session):

    semifinal_one_ceremony = 1
    semifinal_two_ceremony = 2

    simulation_songs_ids = [song.song_id for song in build_simulation_songs(number_of_songs=20)]

    mocker.patch.object(CeremonyService, 'add_songs_to_ceremony')
    add_songs_to_ceremony_spy = mocker.spy(CeremonyRepository, 'add_songs_to_ceremony')

    try:
        SimulatorService(mock_session).divide_songs_into_semifinals(semifinal_one_ceremony=semifinal_one_ceremony, 
                                                                    semifinal_two_ceremony=semifinal_two_ceremony, song_ids=simulation_songs_ids)
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

    assert add_songs_to_ceremony_spy.call_count == 2

    add_songs_to_ceremony_args = add_songs_to_ceremony_spy.call_args_list

    print("Args: ", add_songs_to_ceremony_args)

    first_call_args = add_songs_to_ceremony_args[0].kwargs
    second_call_args = add_songs_to_ceremony_args[1].kwargs

    assert first_call_args["ceremony_id"] == semifinal_one_ceremony and second_call_args["ceremony_id"] == semifinal_two_ceremony
    assert len(first_call_args["song_ids"]) + len(second_call_args["song_ids"]) == 20

def test_simulate_ceremony(mocker, mock_session):
    ceremony_id = 2

    simulation_songs = build_simulation_songs(number_of_songs=20)

    mocker.patch.object(SongService, 'get_simulation_songs_by_ceremony_id', return_value=simulation_songs)
    mocker.patch.object(VotingRepository, 'add_votings')
    add_votings_spy = mocker.spy(VotingRepository, 'add_votings')

    try:
        SimulatorService(mock_session).simulate_ceremony(ceremony_id=ceremony_id)
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

    add_votings_spy.assert_called_once()
    kwargs = add_votings_spy.call_args.kwargs

    assert len(kwargs["votings"]) == len(simulation_songs) * 10 * 2 # 20 songs * 10 votings per country * 2 voting types (jury and televote)


def test_generate_scores_by_country(mock_session):

    country_id = 1
    ceremony_id = 2

    simulation_songs = build_simulation_songs(number_of_songs=20) 

    result = SimulatorService(mock_session).generate_scores_by_country(country_id=country_id, ceremony_id=ceremony_id, simulation_songs=simulation_songs)

    assert isinstance(result, list)
    assert len(result) == 20 
    assert len(list(filter(lambda x: x["voting_type_id"] == constants.JURY_VOTING_TYPE_ID, result))) == 10
    assert len(list(filter(lambda x: x["voting_type_id"] == constants.TELEVOTE_VOTING_TYPE_ID, result))) == 10

    assert country_id not in [score["country_id"] for score in result]


def build_simulation_songs(number_of_songs):
    return [SimulationSong(song_id=i, 
                           country_id=i, 
                           jury_potential_score=random.randint(1, 10), 
                           televote_potential_score=random.randint(1, 10))
        for i in range(1, number_of_songs + 1)]

    
    



