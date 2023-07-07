from typing import Any
from pydantic import BaseModel
from pydantic.fields import Field

class SchemaId(BaseModel):
    id: int = Field(..., description="Id", example=1)

class ResultResponse(BaseModel):
    message: str = Field(..., description="Message", example="Success")
    data: Any = None


class ErrorResponse(BaseModel):
    message: str