import collections
from sqlalchemy import Sequence
from app.logic.models import Ceremony, CeremonyType, Country, Event, Participant, ParticipantResult, SimulationCeremonyResult, SimulationSong, Song, Voting, VotingType
from app.persistence.entities import CeremonyEntity, CeremonyTypeEntity, CountryEntity, EventEntity, SongEntity, VotingEntity, VotingTypeEntity, SongCeremony

class CeremonyModelMapper:

    def map_to_ceremony_entity(self, ceremony: Ceremony)->CeremonyEntity:
        return CeremonyEntity(id=ceremony.id, ceremony_type_id=ceremony.ceremony_type.id, 
                            event_id=ceremony.event.id, date=ceremony.date)
    
    def map_to_ceremony_model_without_event(self, ceremony_entity: CeremonyEntity)->Ceremony:
        if ceremony_entity is None:
            return None
        ceremony_type = CeremonyModelMapper().map_to_ceremony_type_model(ceremony_entity.ceremony_type)
        ceremony_songs = [SongModelMapper().map_to_song_with_country_model(song) for song in ceremony_entity.songs]
        ceremony_votings = [VotingModelMapper().map_to_voting_model_without_ceremony(voting) for voting in ceremony_entity.votings]
        return Ceremony(id=ceremony_entity.id, date=ceremony_entity.date, ceremony_type=ceremony_type, 
                        songs=ceremony_songs, votings=ceremony_votings)
    

    def map_to_ceremony_type_model(self, ceremony_type_entity: CeremonyTypeEntity)->CeremonyType:
        return CeremonyType(id=ceremony_type_entity.id, name=ceremony_type_entity.name, code=ceremony_type_entity.code)
    
    def map_to_ceremony_map(self, rows: Sequence)->dict[int, int]:
        return {row.ceremony_type_id:row.id for row in rows}


class SongModelMapper:

    CountrySong = collections.namedtuple('CountrySong', ['song_id', 'country_id'])

    def map_to_song_entity(self, song: Song)->SongEntity:
        
        country_entity = CountryModelMapper().map_to_country_entity(song.country)
        event_entity = EventModelMapper().map_to_event_entity(song.event)
        return SongEntity(id=song.id, title=song.title, artist=song.artist, 
                            jury_potential_score=song.jury_potential_score, 
                            televote_potential_score=song.televote_potential_score,
                            belongs_to_host_country=song.belongs_to_host_country,
                            country=country_entity, event=event_entity,
                            country_id=country_entity.id, event_id=event_entity.id)
    

    def map_to_song_model_without_submodels(self, song_entity: SongEntity)->Song:
        if song_entity is None:
            return None
        
        return Song(id=song_entity.id, title=song_entity.title, artist=song_entity.artist, 
                    jury_potential_score=song_entity.jury_potential_score, 
                    televote_potential_score=song_entity.televote_potential_score,
                    belongs_to_host_country=song_entity.belongs_to_host_country)
    
    def map_to_song_with_country_model(self, song_entity: SongEntity)->Song:
        country = CountryModelMapper().map_to_country_model_without_submodels(country_entity=song_entity.country)
        song = self.map_to_song_model_without_submodels(song_entity=song_entity)
        if song is not None:
            song.country = country

        return song

    def map_to_song_model(self, song_entity: SongEntity)->Song:
        event = EventModelMapper().map_to_event_model_without_submodels(event_entity=song_entity.event)
        country = CountryModelMapper().map_to_country_model_without_submodels(country_entity=song_entity.country)
        Song.model_rebuild()
        song = self.map_to_song_model_without_submodels(song_entity=song_entity)
        if song is not None:
            song.country = country
            song.event = event

        return song
    
    def map_to_simulation_song_model_list(self, rows: Sequence)->list[SimulationSong]:
        return [SimulationSong(song_id=row.id, country_id=row.country_id, jury_potential_score=row.jury_potential_score, 
                               televote_potential_score=row.televote_potential_score) for row in rows]

    def map_to_song_country_ids(self, rows: Sequence)->CountrySong:
        return [self.CountrySong(song_id=row.id, country_id=row.country_id) for row in rows]

class CountryModelMapper:

    def map_to_country_entity(self, country: Country)->CountryEntity:
        return CountryEntity(id=country.id, name=country.name, code=country.code)
    

    def map_to_country_model_without_submodels(self, country_entity: CountryEntity)->Country:
        if country_entity is None:
            return None
        return Country(id=country_entity.id, name=country_entity.name, code=country_entity.code)


    def map_to_country_model(self, country_entity: CountryEntity)->Country:
        songs = [SongModelMapper().map_to_song_model_without_submodels(song) for song in country_entity.songs]
        country = self.map_to_country_model_without_submodels(country_entity=country_entity)
        if country is not None:
            country.songs = songs

        return country


class EventModelMapper:

    def map_to_event_entity(self, event: Event)->EventEntity:
        return EventEntity(id=event.id, year=event.year, slogan=event.slogan, host_city=event.host_city, arena=event.arena) 


    def map_to_event_model_without_submodels(self, event_entity: EventEntity)->Event:
        if event_entity is None:
            return None
        return Event(id=event_entity.id, year=event_entity.year, slogan=event_entity.slogan, 
                    host_city=event_entity.host_city, arena=event_entity.arena)
    
    
    def map_to_event_model(self, event_entity: EventEntity)->Event:
        ceremonies = [CeremonyModelMapper().map_to_ceremony_model_without_event(ceremony) for ceremony in event_entity.ceremonies]
        event = self.map_to_event_model_without_submodels(event_entity=event_entity)
        if event is not None:
            event.ceremonies = ceremonies

        return event

class VotingModelMapper:

    def map_to_voting_type_model(self, voting_type_entity: VotingTypeEntity)->VotingType:
        return VotingType(id=voting_type_entity.id, name=voting_type_entity.name)

    def map_to_voting_model_without_ceremony(self, voting_entity: VotingEntity)->Voting:
        voting_type = self.map_to_voting_type_model(voting_entity.voting_type)
        song = SongModelMapper().map_to_song_with_country_model(song_entity=voting_entity.song)
        country = CountryModelMapper().map_to_country_model_without_submodels(country_entity=voting_entity.country)

        return Voting(id=voting_entity.id, score=voting_entity.score, voting_type=voting_type, song=song, country=country)
    

class SimulationModelMapper:

    def map_to_participant_result_model(self, row: Sequence)->ParticipantResult:
        voting = row[0]
        voted_song = SongModelMapper().map_to_song_with_country_model(song_entity=voting.song)

        participant_info = self.build_participant_info_model_by_song(song=voted_song)

        return ParticipantResult(country_id=voted_song.country.id, 
                                 song_id=voted_song.id, participant_info=participant_info, 
                                 jury_score=row[1], televote_score=row[2], total_score=row [3])
    
    def map_to_simulation_ceremony_result_model_list(self, rows: Sequence)->list[SimulationCeremonyResult]:

        simulation_results_by_ceremony = {}

        for row in rows:
            simulation_by_ceremony = simulation_results_by_ceremony.get(row.ceremony_id)

            if simulation_by_ceremony is None:
                simulation = SimulationCeremonyResult(ceremony_id=row.ceremony_id, ceremony_type=CeremonyType(id=row.ceremony_type_id, name=row.ceremony_type_name))

                participant_result = self.build_participant_result(row=row)
                
                simulation.results.append(participant_result)

                simulation_results_by_ceremony[row.ceremony_id] = simulation

            else:

                participant_result = self.build_participant_result(row=row)
                
                simulation_by_ceremony.results.append(participant_result)

        return list(simulation_results_by_ceremony.values())
    
    def map_to_simulation_ceremony_result_model(self, rows: Sequence)->SimulationCeremonyResult:
        simulation = SimulationCeremonyResult(ceremony_id=rows[0].ceremony_id, ceremony_type=CeremonyType(id=rows[0].ceremony_type_id, name=rows[0].ceremony_type_name))

        for row in rows:
            participant_result = self.build_participant_result(row=row)
            simulation.results.append(participant_result)

        return simulation



    def build_participant_info_model_by_song(self, song: Song)->Participant:

        participant_info = f"{song.country.name}. {song.artist} - {song.title}. Jury potential score: {song.jury_potential_score} | Televote potential score: {song.televote_potential_score}"
        return Participant(country_id=song.country.id, song_id=song.id, participant_info=participant_info)
    
    def build_participant_info(self, country_name: str, 
                               artist: str, title: str, jury_potential_score: int, 
                               televote_potential_score: int)->str:
        
        return f"{country_name}. {artist} - {title}. Jury potential score: {jury_potential_score} | Televote potential score: {televote_potential_score}"

    
    def build_participant_result(self, row)->ParticipantResult:
        participant_info = self.build_participant_info(country_name=row.country_name, artist=row.song_artist,
        title=row.song_title, jury_potential_score=row.jury_potential_score,televote_potential_score=row.televote_potential_score)
        
        return ParticipantResult(country_id=row.country_id, song_id=row.song_id, participant_info=participant_info, jury_score=row.jury_score,
        televote_score=row.televote_score, total_score=row.total_score)

        
    