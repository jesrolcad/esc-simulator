from app.logic.models import Participant
from app.routers.schemas.simulator_schemas import ParticipantDataResponse


class SimulatorApiMapper:

    def map_to_participant_data_response(self, participant_model: Participant)->ParticipantDataResponse:
        return ParticipantDataResponse(country_id=participant_model.country_id, song_id=participant_model.song_id, 
                                        participant_info=participant_model.participant_info)
