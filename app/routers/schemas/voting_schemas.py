from app.routers.schemas.base_schemas import BaseId, BaseVotingType, BaseVoting


class VotingTypeDataResponse(BaseVotingType, BaseId):
    pass


class VotingDataResponse(BaseVoting, BaseId):
    voting_type: VotingTypeDataResponse


