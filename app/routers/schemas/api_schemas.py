from typing import Any, Optional
from pydantic import BaseModel
from pydantic.fields import Field
import strawberry

class ResultResponse(BaseModel):
    message: str = Field(..., json_schema_extra={"description":"Message", "example":"Success"})
    data: Any = None

class ErrorDetailResponse(BaseModel):
    field: Optional[str] = Field(None, json_schema_extra={"description": "Field in which the error occurred", "example": "title"})
    message: str = Field(..., json_schema_extra={"description":"Error message", "example":"Field required"})

class ErrorResponse(BaseModel):
    errors: list[ErrorDetailResponse] = Field([], json_schema_extra={"description":"List of errors", "example":[{"field": "title", "message": "Field required"}]})

@strawberry.type
class ResultResponseQL:
    success: bool
    message: str