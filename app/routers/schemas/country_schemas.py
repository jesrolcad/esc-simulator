from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str
    code: str

class CountryCreateRequest(CountryBase):
    pass