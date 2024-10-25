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

create_update_song_positive_test_cases = [
    {
        "title": "a",
        "artist": "a",
        "belongs_to_host_country": False,
        "jury_potential_score": 10,
        "televote_potential_score": 10,
        "country_id": 1,
        "event_id": 1
    },

    {
        "title": "50char50char50char50char50char50char50char50char50",
        "artist": "50char50char50char50char50char50char50char50char50",
        "belongs_to_host_country": True,
        "jury_potential_score": 1,
        "televote_potential_score": 1,
        "country_id": 1,
        "event_id": 1
    }
]

create_update_song_mutation_positive_test_cases = [
    {
        "title": "a",
        "artist": "a",
        "belongs_to_host_country": "false",
        "jury_potential_score": "TEN",
        "televote_potential_score": "TEN",
        "country_id": 1,
        "event_id": 1
    },

    {
        "title": "50char50char50char50char50char50char50char50char50",
        "artist": "50char50char50char50char50char50char50char50char50",
        "belongs_to_host_country": "true",
        "jury_potential_score": "ONE",
        "televote_potential_score": "ONE",
        "country_id": 1,
        "event_id": 1
    }

]

create_update_song_negative_test_cases = [
    {
        "case": "empty_body_none_fields",
        "body": {},
        "invalid_fields": ["title", "artist", "belongs_to_host_country", "jury_potential_score", "televote_potential_score", "country_id", "event_id"]
    },

    {
        "case": "empty_title_and_artist",
        "body": {
            "title": "",
            "artist": "",
            "belongs_to_host_country": False,
            "jury_potential_score": 10,
            "televote_potential_score": 10,
            "country_id": 1,
            "event_id": 1
        },
        "invalid_fields": ["title", "artist"]
    },

    {
        "case": "blank_title_and_artist",
        "body": {
            "title": "   ",
            "artist": "   ",
            "belongs_to_host_country": False,
            "jury_potential_score": 10,
            "televote_potential_score": 10,
            "country_id": 1,
            "event_id": 1
        },

        "invalid_fields": ["title", "artist"]
    },


    {
        "case": "max_length_title_and_artist_exceeded",
        "body": {
            "title": "51char51char51char51char51char51char51char51char51c",
            "artist": "51char51char51char51char51char51char51char51char51c",
            "belongs_to_host_country": False,
            "jury_potential_score": 10,
            "televote_potential_score": 10,
            "country_id": 1,
            "event_id": 1
        },

        "invalid_fields": ["title", "artist"]
        },

    {
        "case": "invalid_values_potential_scores",
        "body": {
            "title": "TEST CREATE",
            "artist": "TEST CREATE",
            "belongs_to_host_country": False,
            "jury_potential_score": 0,
            "televote_potential_score": 0,
            "country_id": 1,
            "event_id": 1
        },
        "invalid_fields": ["jury_potential_score", "televote_potential_score"]

    }, 

    {
        "case": "invalid_values_potential_scores",
        "body": {
            "title": "TEST CREATE",
            "artist": "TEST CREATE",
            "belongs_to_host_country": False,
            "jury_potential_score": 11,
            "televote_potential_score": 11,
            "country_id": 1,
            "event_id": 1
        },
        "invalid_fields": ["jury_potential_score", "televote_potential_score"]
    },

    {
        "case": "non_existent_country",
        "body": {
            "title": "a",
            "artist": "a",
            "belongs_to_host_country": False,
            "jury_potential_score": 10,
            "televote_potential_score": 10,
            "country_id": 0,
            "event_id": 1
        },
        "invalid_fields": ["country_id"]
    }, 

    {
        "case": "non_existent_event",
        "body": {
            "title": "a",
            "artist": "a",
            "belongs_to_host_country": False,
            "jury_potential_score": 10,
            "televote_potential_score": 10,
            "country_id": 1,
            "event_id": 0
        },
        "invalid_fields": ["event_id"]
    }, 

    {
        "case": "non_existent_country_and_event",
        "body": {
            "title": "a",
            "artist": "a",
            "belongs_to_host_country": False,
            "jury_potential_score": 10,
            "televote_potential_score": 10,
            "country_id": 0,
            "event_id": 0
        },
        "invalid_fields": ["country_id, event_id"]
    },

    {
        "case": "existing_song_by_country_and_event",
        "body": {
            "title": "a",
            "artist": "a",
            "belongs_to_host_country": False,
            "jury_potential_score": 10,
            "televote_potential_score": 10,
            "country_id": 1,
            "event_id": 1
        },

        "invalid_fields": ["country_id, event_id"]
    }, 

    {
        "case": "create_another_song_belongs_to_host_country",
        "body": {
            "title": "a",
            "artist": "a",
            "belongs_to_host_country": True,
            "jury_potential_score": 10,
            "televote_potential_score": 10,
            "country_id": 2,
            "event_id": 1
        },

        "invalid_fields": ["belongs_to_host_country"]
    },

    {
        "case": "update_another_song_belongs_to_host_country",
        "body": {
            "title": "a",
            "artist": "a",
            "belongs_to_host_country": True,
            "jury_potential_score": 10,
            "televote_potential_score": 10,
            "country_id": 1,
            "event_id": 2
        },
        "invalid_fields": ["belongs_to_host_country"]
    }
]

create_update_song_mutation_negative_test_cases = [
    {
        "title": "",
        "artist": "",
        "belongs_to_host_country": "false",
        "jury_potential_score": "TEN",
        "televote_potential_score": "TEN",
        "country_id": 1,
        "event_id": 1
    },

    {
        "title": "   ",
        "artist": "   ",
        "belongs_to_host_country": "false",
        "jury_potential_score": "TEN",
        "televote_potential_score": "TEN",
        "country_id": 1,
        "event_id": 1
    },


    {
        "title": "51char51char51char51char51char51char51char51char51c",
        "artist": "51char51char51char51char51char51char51char51char51c",
        "belongs_to_host_country": "false",
        "jury_potential_score": "TEN",
        "televote_potential_score": "TEN",
        "country_id": 1,
        "event_id": 1
    },

    {
        "title": "TEST CREATE",
        "artist": "TEST CREATE",
        "belongs_to_host_country": "false",
        "jury_potential_score": "ZERO",
        "televote_potential_score": "ZERO",
        "country_id": 1,
        "event_id": 1
    },

    {
        "title": "TEST CREATE",
        "artist": "TEST CREATE",
        "belongs_to_host_country": "false",
        "jury_potential_score": "ELEVEN",
        "televote_potential_score": "ELEVEN",
        "country_id": 1,
        "event_id": 1
    },

    {
        "title": "a",
        "artist": "a",
        "belongs_to_host_country": "false",
        "jury_potential_score": "TEN",
        "televote_potential_score": "TEN",
        "country_id": 0,
        "event_id": 1
    }
]