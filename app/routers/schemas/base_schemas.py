from typing import Literal
from datetime import date as date_type
from pydantic import BaseModel, Field, field_validator
from . import validation_utils


class BaseId(BaseModel):
    id: int = Field(..., json_schema_extra={"description":"Id", "example":1})


class BaseSong(BaseModel):
    title: str = Field(..., json_schema_extra={"description":"Song title", "example":"La, la, la"}, min_length=1, max_length=50)
    artist: str = Field(..., json_schema_extra={"description":"Artist name", "example":"Massiel"}, min_length=1, max_length=50)
    belongs_to_host_country: bool = Field(..., json_schema_extra={"description":"Whether the song belongs to the host country or not", "example":False})
    jury_potential_score: Literal[1,2,3,4,5,6,7,8,9,10] = Field(..., json_schema_extra={"description":"Factor to calculate the jury score", "example":10})
    televote_potential_score: Literal[1,2,3,4,5,6,7,8,9,10] =  Field(..., json_schema_extra={"description":"Factor to calculate the televote score", "example":10})

    @field_validator("title", "artist")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)


class  BaseCountry(BaseModel):
    name: str = Field(..., json_schema_extra={"description":"Country name", "example":"Spain"}, min_length=3, max_length=50)
    code: str = Field(..., json_schema_extra={"description":"Country code", "example":"ESP"}, min_length=3, max_length=5)

    @field_validator("name", "code")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)


class BaseEvent(BaseModel):
    year: int = Field(..., ge=0, json_schema_extra={"description":"Event year", "example":2018})
    slogan: str = Field(..., json_schema_extra={"description":"Event slogan", "example":"All Aboard!"}, min_length=1, max_length=50)
    host_city: str = Field(..., json_schema_extra={"description":"Event host city", "example":"Lisbon"}, min_length=1, max_length=50)
    arena: str = Field(..., json_schema_extra={"description":"Event arena", "example":"Altice Arena"}, min_length=1, max_length=50)

    @field_validator("slogan", "host_city", "arena")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)

class BaseCeremonyType(BaseModel):
    name: str = Field(..., json_schema_extra={"description":"Ceremony type name", "example":"Semifinal 1"}, min_length=1, max_length=50)
    code: str = Field(..., json_schema_extra={"description":"Ceremony type code", "example":"SF1"}, min_length=1, max_length=5)

    @field_validator("name", "code")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)

class BaseCeremony(BaseModel):

    date: date_type = Field(..., json_schema_extra={"description":"Ceremony date", "example":"2023-05-13"})


class BaseVotingType(BaseModel):
    name: str = Field(..., json_schema_extra={"description":"Voting type name", "example":"Jury"}, min_length=1, max_length=50)

    @field_validator("name")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)

class BaseVoting(BaseModel):
    score: Literal[1, 2, 3, 4, 5, 6, 7, 8, 10, 12] = Field(..., json_schema_extra={"description":"Voting score", "example":12})


class BaseParticipant(BaseModel):
    country_id: int = Field(..., json_schema_extra={"description":"Country id", "example":1})
    song_id: int = Field(..., json_schema_extra={"description":"Song id", "example":1})
    participant_info: str = Field(..., json_schema_extra={"description":"Participant info", "example":"Spain. Massiel - La, la, la. Jury potential score: 10 | Televote potential score: 10"}, min_length=1, max_length=200)

    @field_validator("participant_info")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)


class BaseSimulationResult(BaseModel):
    ceremony_id: int = Field(..., json_schema_extra={"description":"Ceremony id", "example":1})

