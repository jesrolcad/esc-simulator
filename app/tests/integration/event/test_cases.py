from datetime import datetime, timedelta

grand_final_date = datetime.now()
grand_final_date_str = grand_final_date.strftime("%Y-%m-%d")
sf1_date = grand_final_date - timedelta(days=4)
sf1_date_str = sf1_date.strftime("%Y-%m-%d")
sf2_date = grand_final_date - timedelta(days=2)
sf2_date_str = sf2_date.strftime("%Y-%m-%d")
year = datetime.now().year


expected_get_events_response = {
        "id": 1,
        "year": 1,
        "slogan": "EVENT",
        "host_city": "HOST_CITY",
        "arena": "ARENA",
        "ceremonies": [
            {
                "id": 1,
                "date": sf1_date_str,
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

expected_event_query_response = {
        "id": 1,
        "year": 1,
        "slogan": "EVENT",
        "hostCity": "HOST_CITY",
        "arena": "ARENA",
        "ceremonies": [
            {
                "id": 1,
                "date": sf1_date.strftime("%Y-%m-%dT00:00:00"),
                "ceremonyType": {
                    "id": 1,
                    "name": "SEMIFINAL 1",
                    "code": "SF1"
                }
            }
        ]
    }


expected_get_event_ceremony_response = {
                "id": 1,
                "date": sf1_date_str,
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

create_update_event_positive_test_cases = [
    {
        "year": year,
        "slogan": "EVENT",
        "host_city": "HOST_CITY",
        "arena": "ARENA",
        "grand_final_date": grand_final_date_str,
    },
    
    {
        "year": year,
        "slogan": "E",
        "host_city": "H",
        "arena": "A",
        "grand_final_date": grand_final_date_str,
    },
    
    {
        "year": year,
        "slogan": "E" * 50,
        "host_city": "H" * 50,
        "arena": "A" * 50,
        "grand_final_date": grand_final_date_str,
    }
]


create_event_negative_test_cases = [

    {
        "case": "empty_body_none_fields",
        "body": {},
        "invalid_fields": ["year", "slogan", "host_city", "arena", "grand_final_date"]
    }, 

    {
        "case": "blank_str_fields",
        "body": {
            "year": year,
            "slogan": "   ",
            "host_city": "   ",
            "arena": "   ",
            "grand_final_date": grand_final_date_str
        },
        "invalid_fields": ["slogan", "host_city", "arena"]
    },

    {
        "case": "not_a_year",
        "body": {
            "year": "not a year",
            "slogan": "EVENT",
            "host_city": "HOST_CITY",
            "arena": "ARENA",
            "grand_final_date": grand_final_date_str
        },
        "invalid_fields": ["year"]

    },

    {
        "case": "not_a_date",
        "body": {
            "year": year,
            "slogan": "EVENT",
            "host_city": "HOST_CITY",
            "arena": "ARENA",
            "grand_final_date": "not a date"
        },
        "invalid_fields": ["grand_final_date"]
    },

    {
        "case": "more_than_50_characters_str_fields",
        "body": {
            "year": year,
            "slogan": "E" * 51,
            "host_city": "H" * 51,
            "arena": "A" * 51,
            "grand_final_date": grand_final_date_str
        },
        "invalid_fields": ["slogan", "host_city", "arena"]
    }
]

create_event_mutation_negative_test_cases = [

    {
        "year": year,
        "slogan": "   ",
        "host_city": "   ",
        "arena": "   ",
        "grand_final_date": grand_final_date_str
    },

    {
        "year": "not a year",
        "slogan": "EVENT",
        "host_city": "HOST_CITY",
        "arena": "ARENA",
        "grand_final_date": grand_final_date_str
    },

    {
        "year": -1,
        "slogan": "EVENT",
        "host_city": "HOST_CITY",
        "arena": "ARENA",
        "grand_final_date": grand_final_date_str
    },

    {
        "year": year,
        "slogan": "EVENT",
        "host_city": "HOST_CITY",
        "arena": "ARENA",
        "grand_final_date": "not a date"
    },

    {
        "year": year,
        "slogan": "EVENT",
        "host_city": "HOST_CITY",
        "arena": "ARENA",
        "grand_final_date": grand_final_date_str
    },

    {
        "year": year,
        "slogan": "E" * 51,
        "host_city": "H" * 51,
        "arena": "A" * 51,
        "grand_final_date": "2021-01-01"
    }
]

update_event_negative_test_cases = [

    {
        "case": "empty_body_none_fields",
        "body": {},
        "invalid_fields": ["slogan", "host_city", "arena"]
    }, 

    {
        "case": "blank_str_fields",
        "body": {
            "slogan": "   ",
            "host_city": "   ",
            "arena": "   "
        },
        "invalid_fields": ["slogan", "host_city", "arena"]
    },

    {
        "case": "more_than_50_characters_str_fields",
        "body": {
            "slogan": "E" * 51,
            "host_city": "H" * 51,
            "arena": "A" * 51
        },
        "invalid_fields": ["slogan", "host_city", "arena"]
    }
]

update_event_mutation_negative_test_cases = [

    {
        "slogan": "   ",
        "host_city": "   ",
        "arena": "   "
    },

    {
        "slogan": "E" * 51,
        "host_city": "H" * 51,
        "arena": "A" * 51
    }
]

