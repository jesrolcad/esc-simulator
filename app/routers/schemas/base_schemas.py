from typing import Any
from pydantic import BaseModel

class ResultResponse(BaseModel):
    message: str
    data: Any = None


class ErrorResponse(BaseModel):
    message: str