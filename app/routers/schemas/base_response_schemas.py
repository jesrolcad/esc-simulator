from typing import Any
from pydantic import BaseModel

class ResultResponse(BaseModel):
    success: bool
    message: str
    data: Any = None