from pydantic import BaseModel

class YearRequest(BaseModel):
    years: list[int]