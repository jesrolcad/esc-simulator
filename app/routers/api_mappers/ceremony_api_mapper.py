from app.logic.models import Ceremony
from app.routers.schemas.common_schemas import CeremonyWithoutEventDataResponse, CeremonyTypeDataResponse, SongWithCountryDataResponse, CountryWithoutSongsVotingsDataResponse, VotedSong, VotingCountry, VotingTypeDataResponse, VotingWithoutCeremonyEvent

class CeremonyApiMapper:

    def map_to_ceremony_without_event_data_response(self, ceremony: Ceremony)->CeremonyWithoutEventDataResponse:
        ceremony_type = CeremonyTypeDataResponse(id=ceremony.ceremony_type.id, name=ceremony.ceremony_type.name, code=ceremony.ceremony_type.code)
        songs = []
        for song in ceremony.songs:
            country = country = CountryWithoutSongsVotingsDataResponse(id=song.country.id, name=song.country.name, code=song.country.code)
            songs.append(SongWithCountryDataResponse(id=song.id, title=song.title, artist=song.artist, belongs_to_host_country=song.belongs_to_host_country, jury_potential_score=song.jury_potential_score, televote_potential_score=song.televote_potential_score, country=country))
        votings = []
        for voting in ceremony.votings:
            voting_country = VotingCountry(id=voting.country.id, name=voting.country.name)
            voted_song = VotedSong(id=voting.song.id, title=voting.song.title, country_id=voting.song.country.id, country_name=voting.song.country.name)
            voting_type = VotingTypeDataResponse(id=voting.voting_type.id, name=voting.voting_type.name)
            votings.append(VotingWithoutCeremonyEvent(id=voting.id, score=voting.score, voting_country=voting_country, voted_song=voted_song, voting_type=voting_type))

        return CeremonyWithoutEventDataResponse(id=ceremony.id, date=ceremony.date, ceremony_type=ceremony_type, songs=songs, votings=votings)