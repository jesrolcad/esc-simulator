import datetime
from typing import List
from datetime import date
from pydantic import Field, ValidationInfo, field_validator, BaseModel, model_validator
import strawberry
from app.routers.schemas import validation_utils
from app.routers.schemas.base_schemas import BaseEventQL, BaseId, BaseEvent
from app.routers.schemas.common_schemas import CeremonyWithoutEventDataResponse
from app.utils.exceptions import BusinessLogicValidationError


class EventDataResponse(BaseEvent, BaseId): 
    ceremonies: List[CeremonyWithoutEventDataResponse] = []

class EventDataResponseList(BaseModel):
    events: List[EventDataResponse]

class CreateEventRequest(BaseEvent):
    grand_final_date: date = Field(..., json_schema_extra={"description":"Grand Final ceremony date", "example":"2020-05-16"})

    @field_validator("grand_final_date")
    @classmethod
    def validate_date_not_past(cls, field: date)->date:
        if field < date.today():
            raise ValueError("Date cannot be in the past.")
        return field

    @model_validator(mode="after")
    def validate_year_and_grand_final_date(self):
        if self.year != self.grand_final_date.year:
            raise ValueError("Year cannot be different from grand final date year.")
        return self
    
    @field_validator("year")
    @classmethod
    def validate_year_not_in_past(cls, field: int)->int:
        if field < datetime.datetime.today().year:
            raise BusinessLogicValidationError(field="year", message="Year cannot be in the past.")
        return field


class UpdateEventRequest(BaseModel):
    slogan: str = Field(..., json_schema_extra={"description":"Event slogan", "example":"All Aboard!"}, min_length=1, max_length=50)
    host_city: str = Field(..., json_schema_extra={"description":"Event host city", "example":"Lisbon"}, min_length=1, max_length=50)
    arena: str = Field(..., json_schema_extra={"description":"Event arena", "example":"Altice Arena"}, min_length=1, max_length=50)

    @field_validator("slogan", "host_city", "arena")
    @classmethod
    def validate_str_not_blank(cls, field: str)->str:
        return validation_utils.validate_str_not_blank(field)

@strawberry.input
class CreateEventRequestQL(BaseEventQL):
    grand_final_date: date

@strawberry.input
class UpdateEventRequestQL:
    slogan: str
    host_city: str
    arena: str