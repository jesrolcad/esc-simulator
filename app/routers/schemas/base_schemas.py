from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from . import validation_utils


class BaseId(BaseModel):
    id: int = Field(..., description="Id", example=1)


class BaseSong(BaseModel):
    title: str = Field(..., description="Song title", example="La, la, la", min_length=1, max_length=50)
    artist: str = Field(..., description="Artist name", example="Massiel", min_length=1, max_length=50)
    belongs_to_host_country: bool = Field(..., description="Whether the song belongs to the host country or not", example=False)
    jury_potential_score: Literal[1,2,3,4,5,6,7,8,9,10] = Field(..., description="Factor to calculate the jury score", example=10)
    televote_potential_score: Literal[1,2,3,4,5,6,7,8,9,10] =  Field(..., description="Factor to calculate the televote score", example=10)

    @field_validator("title", "artist")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)


class  BaseCountry(BaseModel):
    name: str = Field(..., description="Country name", example="Spain", min_length=3, max_length=50)
    code: str = Field(..., description="Country code", example="ESP", min_length=3, max_length=5)

    @field_validator("name", "code")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)


class BaseEvent(BaseModel):
    year: int = Field(..., description="Event year", example=2018)
    slogan: str = Field(..., description="Event slogan", example="All Aboard!", min_length=1, max_length=50)
    host_city: str = Field(..., description="Event host city", example="Lisbon", min_length=1, max_length=50)
    arena: str = Field(..., description="Event arena", example="Altice Arena", min_length=1, max_length=50)

    @field_validator("slogan", "host_city", "arena")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)

class BaseCeremonyType(BaseModel):
    name: str = Field(..., description="Ceremony type name", example="Semifinal 1", min_length=1, max_length=50)
    code: str = Field(..., description="Ceremony type code", example="SF1", min_length=1, max_length=5)

    @field_validator("name", "code")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)

class BaseCeremony(BaseModel):
    date: datetime = Field(..., description="Ceremony date", example="2023-05-13")


class BaseVotingType(BaseModel):
    name: str = Field(..., description="Voting type name", example="Jury", min_length=1, max_length=50)

    @field_validator("name")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)

class BaseVoting(BaseModel):
    score: Literal[1, 2, 3, 4, 5, 6, 7, 8, 10, 12] = Field(..., description="Voting score", example=12)


