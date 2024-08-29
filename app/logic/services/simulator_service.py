import random
from app.logic.models import Participant, SimulationCeremonyResult, SimulationSong
from app.logic.services.base_service import BaseService
from app.logic.services.ceremony_service import CeremonyService
from app.logic.services.song_service import SongService
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.persistence.repositories.song_repository import SongRepository
from app.persistence.repositories.voting_repository import VotingRepository
from app.logic.model_mappers import CeremonyModelMapper, SimulationModelMapper
from app.utils.exceptions import NotFoundError
from app.utils import constants


class SimulatorService(BaseService):

    def get_simulation_participants_by_event_ceremony(self, event_id: int, ceremony_id: int)->list[Participant]:
        
        ceremony_entity = CeremonyRepository(self.session).get_event_ceremony(event_id=event_id, ceremony_id=ceremony_id)
        ceremony = CeremonyModelMapper().map_to_ceremony_model_without_event(ceremony_entity=ceremony_entity)

        if ceremony is None:
            return []
        
        return [SimulationModelMapper().build_participant_info_model_by_song(song) for song in ceremony.songs]
    
    def get_simulation_event_results(self, event_id: int)->list[SimulationCeremonyResult]:
        results = VotingRepository(self.session).get_scores_by_event_id(event_id=event_id)


        if results is None:
            return []

        return SimulationModelMapper().map_to_simulation_ceremony_result_model_list(results)
    
    def get_simulation_event_results_by_ceremony_type(self, event_id: int, ceremony_type_id: int)->SimulationCeremonyResult:

        result = VotingRepository(self.session).get_scores_by_event_id_and_ceremony_type_id(event_id=event_id, ceremony_type_id=ceremony_type_id)

        if result is None or len(result) == 0:
            raise NotFoundError(field="event_id, ceremony_type_id", message=f"No results found for event_id {event_id} and ceremony_type_id {ceremony_type_id}")


        return SimulationModelMapper().map_to_simulation_ceremony_result_model(result) if result else None
    
    def create_simulation(self, event_id: int):
        
        # Get songs which will participate in semifinals
        simulation_songs = SongService(self.session).get_simulation_songs_by_event_id(event_id=event_id)

        if not simulation_songs:
            raise NotFoundError(field="event_id", message=f"No songs found for event_id {event_id}")
        
        # Get ceremonies by event id
        ceremonies = CeremonyService(self.session).get_event_ceremonies(event_id=event_id)

        if not ceremonies:
            raise NotFoundError(field="event_id", message=f"No ceremonies found for event_id {event_id}")
        
         # Delete previous simulation data
        ceremony_ids = list(ceremonies.values())
        
        VotingRepository(self.session).delete_votings_by_ceremonies(ceremonies=ceremony_ids)

        SongRepository(self.session).delete_songs_from_ceremonies(ceremonies=ceremony_ids)

        semifinal_one_ceremony = ceremonies[constants.FIRST_SEMIFINAL_CEREMONY_TYPE_ID]
        semifinal_two_ceremony = ceremonies[constants.SECOND_SEMIFINAL_CEREMONY_TYPE_ID]
        
        self.divide_songs_into_semifinals(semifinal_one_ceremony=semifinal_one_ceremony, semifinal_two_ceremony=semifinal_two_ceremony, 
                                          song_ids=[simulation_song.song_id for simulation_song in simulation_songs])

        # Simulate each semifinal
        self.simulate_ceremony(ceremony_id=semifinal_one_ceremony)
        self.simulate_ceremony(ceremony_id=semifinal_two_ceremony)

        #Add qualified countries to grand final -> Populate song ceremony table
        qualified_for_grand_final_songs = VotingRepository(self.session).get_qualified_song_ids_for_grand_final(semifinal_one_ceremony_id=semifinal_one_ceremony, 
                                                                                                  semifinal_two_ceremony_id=semifinal_two_ceremony)
        
        # Select automatic qualifiers for grand final
        automatic_qualified_country_song_ids = SongService(self.session).get_automatic_qualified_songs_for_grand_final_by_event_id(event_id=event_id)
        qualified_for_grand_final_songs.extend([country_song.song_id for country_song in automatic_qualified_country_song_ids])

        CeremonyRepository(self.session).add_songs_to_ceremony(ceremony_id=ceremonies[constants.GRAND_FINAL_CEREMONY_TYPE_ID], song_ids=qualified_for_grand_final_songs)

        # Simulate grand final
        grand_final_voters = [simulation_song.country_id for simulation_song in simulation_songs] + [country_song.country_id for country_song in automatic_qualified_country_song_ids]
        self.simulate_ceremony(ceremony_id=ceremonies[constants.GRAND_FINAL_CEREMONY_TYPE_ID], grand_final_voters = grand_final_voters)

        
    def divide_songs_into_semifinals(self, semifinal_one_ceremony: int, semifinal_two_ceremony: int, song_ids: list[int]):
    
        songs_per_semifinal = len(song_ids) // 2

        random.shuffle(song_ids)

        song_ids_by_ceremony = [(semifinal_one_ceremony, song_ids[:songs_per_semifinal]), (semifinal_two_ceremony, song_ids[songs_per_semifinal:])]

        for ceremony, songs in song_ids_by_ceremony:
            CeremonyRepository(self.session).add_songs_to_ceremony(ceremony_id=ceremony, song_ids=songs)

    def simulate_ceremony(self, ceremony_id: int, grand_final_voters: list[int] = None):
        if grand_final_voters:
            print(len(grand_final_voters))
            print(grand_final_voters)

        votings = []

        ceremony_songs = SongService(self.session).get_simulation_songs_by_ceremony_id(ceremony_id=ceremony_id)

        voter_country_ids = grand_final_voters if grand_final_voters else [song.country_id for song in ceremony_songs]

        for voter_country_id in voter_country_ids:
            scores_by_country = self.generate_scores_by_country(country_id=voter_country_id, ceremony_id=ceremony_id, simulation_songs=ceremony_songs)
            votings.extend(scores_by_country)

        VotingRepository(self.session).add_votings(votings=votings)
            
    def generate_scores_by_country(self, country_id: int, ceremony_id: int, simulation_songs: list[SimulationSong])->dict:

        scores = []

        jury_scores = []
        televote_scores = []

        for simulation_song in simulation_songs:
            if simulation_song.country_id == country_id:
                continue

            jury_score = {"song_id": simulation_song.song_id, "country_id": simulation_song.country_id, "ceremony_id": ceremony_id, 
                          "voting_type_id": constants.JURY_VOTING_TYPE_ID, 
                          "score": (round(random.random(), 3)) * simulation_song.jury_potential_score}

            televote_score = {"song_id": simulation_song.song_id, "country_id": simulation_song.country_id, "ceremony_id": ceremony_id, 
                            "voting_type_id": constants.TELEVOTE_VOTING_TYPE_ID, 
                            "score": (round(random.random(), 3)) * simulation_song.televote_potential_score}
            

            jury_scores.append(jury_score)
            televote_scores.append(televote_score)

        jury_scores = sorted(jury_scores, key=lambda jury_voting: jury_voting['score'], reverse=True)[:10]
        televote_scores = sorted(televote_scores, key=lambda televote_voting: televote_voting['score'], reverse=True)[:10]
        
        for i, jury_score in enumerate(jury_scores):
            jury_score['score'] = constants.POSSIBLE_POINTS[i]

        for i, televote_score in enumerate(televote_scores):
            televote_score['score'] = constants.POSSIBLE_POINTS[i]

        scores.extend(jury_scores[:10])
        scores.extend(televote_scores[:10])

        return scores
        



    



    