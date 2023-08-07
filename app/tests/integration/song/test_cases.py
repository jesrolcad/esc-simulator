get_songs_test_cases = [
    {
        "case": "empty_list",
        "filter": "",
        "expected_songs_count": 0
    },

    {
        "case": "not_empty_list",
        "filter": "",
        "expected_songs_count": 2
    },

    {
        "case": "filter_by_title",
        "filter": "?title=TEST",
        "expected_songs_count": 1,
    },

    {
        "case": "filter_by_country_code",
        "filter": "?country_code=TEST",
        "expected_songs_count": 1,
    },

    {
        "case": "filter_by_event_year",
        "filter": "?event_year=1",
        "expected_songs_count": 1,
    }, 

    {
        "case": "filter_by_all",
        "filter": "?title=TEST&country_code=TEST&event_year=1",
        "expected_songs_count": 1
    }
]