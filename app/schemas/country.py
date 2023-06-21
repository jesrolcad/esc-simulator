from pydantic import BaseModel


def CountryBase(BaseModel):
    name: str
    code: str

class CountryCreate(CountryBase):
    pass