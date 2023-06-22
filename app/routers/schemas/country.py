from pydantic import BaseModel


def CountryBase(BaseModel):
    name: str
    code: str

class CountryCreateRequest(CountryBase):
    pass