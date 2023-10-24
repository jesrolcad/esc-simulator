expected_get_events_response = {
        "id": 1,
        "year": 1,
        "slogan": "EVENT",
        "host_city": "HOST_CITY",
        "arena": "ARENA",
        "ceremonies": [
            {
                "id": 1,
                "date": "2021-01-01",
                "ceremony_type": {
                    "id": 1,
                    "name": "SEMIFINAL 1",
                    "code": "SF1"
                },
                "songs": [
                    {
                        "id": 1,
                        "title": "SONG1",
                        "artist": "SONG_ARTIST1",
                        "belongs_to_host_country": False,
                        "jury_potential_score": 10,
                        "televote_potential_score": 10,
                        "country": {
                            "id": 1,
                            "name": "COUNTRY",
                            "code": "COU"
                        }
                    },
                    {
                        "id": 2,
                        "title": "SONG2",
                        "artist": "SONG_ARTIST2",
                        "belongs_to_host_country": True,
                        "jury_potential_score": 10,
                        "televote_potential_score": 10,
                        "country": {
                            "id": 2,
                            "name": "COUNTRY2",
                            "code": "CO2"
                        }
                    }
                ],
                "votings": [
                    {
                        "id": 1,
                        "score": 10,
                        "voting_country": {
                            "id": 1,
                            "name": "COUNTRY"
                        },
                        "voted_song": {
                            "id": 2,
                            "title": "SONG2",
                            "country_id": 2,
                            "country_name": "COUNTRY2"
                        },
                        "voting_type": {
                            "id": 1,
                            "name": "JURY"
                        }
                    }
                ]
            }
        ]
    }


get_events_test_cases = [
    {
        "case": "empty_list",
        "expected_event_count": 0,
        "expected_response": []
    },
    {
        "case": "not_empty_list",
        "expected_event_count": 1,
        "expected_response": [expected_get_events_response]
    }
]

