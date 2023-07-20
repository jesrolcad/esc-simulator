from typing import Literal
from pydantic import BaseModel
from pydantic.fields import Field
from app.routers.schemas.api_schemas import SchemaId

class BaseVotingType(BaseModel):
    name: str = Field(..., description="Voting type name", example="Jury")

class VotingTypeDataResponse(BaseVotingType, SchemaId):
    pass


class BaseVoting(BaseModel):
    score: Literal[1, 2, 3, 4, 5, 6, 7, 8, 10, 12] = Field(..., description="Voting score", example=12)
    voting_type: VotingTypeDataResponse


class VotingWithoutCeremonySongCountryDataResponse(BaseVoting, SchemaId):
    pass