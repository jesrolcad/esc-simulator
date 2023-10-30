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