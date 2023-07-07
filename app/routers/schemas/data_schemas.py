from pydantic import BaseModel
from pydantic.fields import Field

class YearRequest(BaseModel):
    years: list[int] = Field(..., description="List of years", example=[2022, 2023])