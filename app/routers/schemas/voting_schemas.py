from pydantic import BaseModel
from typing import Literal
from app.routers.schemas.base_schemas import SchemaId

class BaseVotingType(BaseModel):
    name: str
    code: str

class VotingTypeDataResponse(BaseVotingType, SchemaId):
    pass


class BaseVoting(BaseModel):
    score: Literal[1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
    voting_type: VotingTypeDataResponse


class VotingWithoutCeremonySongCountryDataResponse(BaseVoting, SchemaId):
    pass