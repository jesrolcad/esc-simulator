from app.routers.endpoints.simulator_endpoints import get_event_ceremony_type_results


get_event_ceremony_participants_test_cases = [

    {
        "case": "empty_list",
        "expected_participant_count": 0,
        "expected_response": []
    },

    {
        "case": "not_empty_list",
        "expected_participant_count": 1,
        "expected_response": [
            {
                "country_id": 1,
                "song_id": 1,
                "participant_info": "COUNTRY. SONG_ARTIST1 - SONG1. Jury potential score: 10 | Televote potential score: 10"
            }
        ]
    }
]

get_event_results_test_cases = [

    {
        "case": "empty_list",
        "expected_ceremony_results_count": 0,
        "expected_response": []
    },

    {
        "case": "not_empty_list",
        "expected_ceremony_results_count": 1,
        "expected_response": [
                {
                    "ceremony_id": 1,
                    "ceremony_type_id": 1,
                    "ceremony_type_name": "SEMIFINAL 1",
                    "results": {
                        "participants": [
                            {
                                "country_id": 1,
                                "song_id": 1,
                                "participant_info": "COUNTRY. SONG_ARTIST1 - SONG1. Jury potential score: 10 | Televote potential score: 10",
                                "position": 1,
                                "total_score": 16,
                                "jury_score": 10,
                                "televote_score": 6
                            },
                            {
                                "country_id": 2,
                                "song_id": 2,
                                "participant_info": "COUNTRY2. SONG_ARTIST2 - SONG2. Jury potential score: 8 | Televote potential score: 8",
                                "position": 2,
                                "total_score": 13,
                                "jury_score": 1,
                                "televote_score": 12
                            }
                        ]
                    }
                }
        ]
    }
]

get_event_ceremony_type_results_test_cases = {
            "expected_response": {
                "ceremony_id": 1,
                "ceremony_type_id": 1,
                "ceremony_type_name": "SEMIFINAL 1",
                "results": {
                    "participants": [
                        {
                            "country_id": 1,
                            "song_id": 1,
                            "participant_info": "COUNTRY. SONG_ARTIST1 - SONG1. Jury potential score: 10 | Televote potential score: 10",
                            "position": 1,
                            "total_score": 16,
                            "jury_score": 10,
                            "televote_score": 6
                        },
                        {
                            "country_id": 2,
                            "song_id": 2,
                            "participant_info": "COUNTRY2. SONG_ARTIST2 - SONG2. Jury potential score: 8 | Televote potential score: 8",
                            "position": 2,
                            "total_score": 13,
                            "jury_score": 1,
                            "televote_score": 12
                        }
                    ]
                }
            }
        }
