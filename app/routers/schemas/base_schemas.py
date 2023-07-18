from typing import Any
from pydantic import BaseModel
from pydantic.fields import Field

class SchemaId(BaseModel):
    id: int = Field(..., description="Id", example=1)

class ResultResponse(BaseModel):
    message: str = Field(..., description="Message", example="Success")
    data: Any = None

class ErrorDetailResponse(BaseModel):
    field: str = Field(None, description="Field in which the error occurred", example="title")
    message: str = Field(..., description="Error message", example="Field required")

class ErrorResponse(BaseModel):
    errors: list[ErrorDetailResponse] = Field([], description="List of errors", example=[{"field": "title", "message": "Field required"}])