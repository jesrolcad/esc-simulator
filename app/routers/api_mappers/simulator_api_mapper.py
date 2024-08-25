from app.logic.models import Participant, SimulationCeremonyResult, ParticipantResult
from app.routers.schemas.simulator_schemas import ParticipantDataResponse, SimulationCeremonyResultDataResponse, ParticipantResultDataResponse, ParticipantResultDataResponseList


class SimulatorApiMapper:

    def map_to_participant_data_response(self, participant_model: Participant)->ParticipantDataResponse:
        return ParticipantDataResponse(country_id=participant_model.country_id, song_id=participant_model.song_id, 
                                        participant_info=participant_model.participant_info)
    
    def map_to_participant_result_data_response(self, participant_model: ParticipantResult, position: int)->ParticipantResultDataResponse:

        return ParticipantResultDataResponse(country_id=participant_model.country_id, song_id=participant_model.song_id, 
                                        participant_info=participant_model.participant_info, position=position, total_score=participant_model.total_score,
                                        jury_score=participant_model.jury_score, televote_score=participant_model.televote_score)
    
    def map_to_simulator_ceremony_data_response_list(self, simulation_result_model: list[SimulationCeremonyResult])->list[SimulationCeremonyResultDataResponse]:

        simulations = []

        for simulation in simulation_result_model:

            participant_results_data_response = [self.map_to_participant_result_data_response(participant_result, position) 
                                                for position, participant_result in enumerate(simulation.results, start=1)]
        
            participant_results_list = ParticipantResultDataResponseList(participants=participant_results_data_response)
        
            simulations.append(SimulationCeremonyResultDataResponse(ceremony_id=simulation.ceremony_id, 
                                                    ceremony_type_id=simulation.ceremony_type.id, 
                                                    ceremony_type_name=simulation.ceremony_type.name, 
                                                    results=participant_results_list))
            
        return simulations
    
    def map_to_simulator_ceremony_data_response(self, simulation_result_model: SimulationCeremonyResult)->SimulationCeremonyResultDataResponse:

        participant_results_data_response = [self.map_to_participant_result_data_response(participant_result, position) 
                                                for position, participant_result in enumerate(simulation_result_model.results, start=1)]
        
        participant_results_list = ParticipantResultDataResponseList(participants=participant_results_data_response)
        
        return SimulationCeremonyResultDataResponse(ceremony_id=simulation_result_model.ceremony_id, 
                                                    ceremony_type_id=simulation_result_model.ceremony_type.id, 
                                                    ceremony_type_name=simulation_result_model.ceremony_type.name, 
                                                    results=participant_results_list)


        
        

        