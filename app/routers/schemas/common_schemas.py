from typing import List
import strawberry
from app.routers.schemas.base_schemas import BaseId, BaseIdQL, BaseCountry, BaseSong, BaseSongQL, BaseCeremony, BaseVoting, BaseEvent, BaseCeremonyType, BaseVotingType


class SongWithoutCountryCeremoniesVotings(BaseSong, BaseId):
    pass

@strawberry.type
class SongWithoutCountryCeremoniesVotingsQL(BaseSongQL, BaseIdQL):
    jury_potential_score: int
    televote_potential_score: int


class CountryWithoutSongsVotingsDataResponse(BaseCountry, BaseId):
    pass

@strawberry.experimental.pydantic.type(model=CountryWithoutSongsVotingsDataResponse, all_fields=True)
class CountryWithoutSongsVotingsDataResponseQL:
    pass

class SongWithCountryDataResponse(BaseSong, BaseId):
    country: CountryWithoutSongsVotingsDataResponse

class CeremonyWithoutSongsVotingsDataResponse(BaseCeremony, BaseId):
    pass

class VotingWithoutCeremonySongCountryDataResponse(BaseVoting, BaseId):
    pass

class VotingTypeDataResponse(BaseVotingType, BaseId):
    pass

class VotingCountry(BaseId):
    name: str

class VotedSong(BaseId):
    title: str
    country_id: int
    country_name: str


class VotingWithoutCeremonyEvent(BaseVoting, BaseId):
    voting_country: VotingCountry
    voted_song: VotedSong
    voting_type: VotingTypeDataResponse


class EventWithoutCeremoniesDataResponse(BaseEvent, BaseId):
    pass

class CeremonyTypeDataResponse(BaseCeremonyType, BaseId):
    pass


class CeremonyWithoutEventDataResponse(BaseCeremony, BaseId):
    ceremony_type: CeremonyTypeDataResponse
    songs: List[SongWithCountryDataResponse] = []
    votings: List[VotingWithoutCeremonyEvent] = []
