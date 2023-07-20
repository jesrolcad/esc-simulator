from typing import List
from app.routers.schemas.base_schemas import BaseId, BaseCountry, BaseSong, BaseCeremony, BaseVoting, BaseEvent


class SongWithoutCountryCeremoniesVotings(BaseSong, BaseId):
    pass

class CountryDataResponse(BaseCountry, BaseId):
    songs: List[SongWithoutCountryCeremoniesVotings] = []

class CountryWithoutSongsVotingsDataResponse(BaseCountry, BaseId):
    pass

class CeremonyWithoutSongsVotingsDataResponse(BaseCeremony, BaseId):
    pass

class VotingWithoutCeremonySongCountryDataResponse(BaseVoting, BaseId):
    pass


class EventWithoutCeremoniesDataResponse(BaseEvent, BaseId):
    pass