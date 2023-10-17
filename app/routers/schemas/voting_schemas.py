from app.routers.schemas.base_schemas import BaseId, BaseVoting
from app.routers.schemas.common_schemas import VotingTypeDataResponse


class VotingDataResponse(BaseVoting, BaseId):
    voting_type: VotingTypeDataResponse


