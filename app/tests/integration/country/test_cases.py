
get_countries_test_cases = [
    {
        "case": "empty_list",
        "expected_countries_count": 0,
    },

    {
        "case": "not_empty_list",
        "expected_countries_count": 1,
    }
]

create_update_country_positive_test_cases = [
    {
        "name": "TEST",
        "code": "TEST"
    },

    {
        "name": "aaa",
        "code": "aaa"
    },

    {
        "name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "code": "5CHAR"
    }
]

create_update_country_negative_test_cases = [

    {
        "case": "empty_body",
        "body": {},
        "invalid_fields": ["name", "code"]
    },

    {
        "case": "empty_name_and_code",
        "body": {
            "name": "",
            "code": ""
        },
        "invalid_fields": ["name", "code"]

    },

    {
        "case": "empty_code",
        "body": {
            "name": "TEST",
            "code": ""
        },
        "invalid_fields": ["code"]
    },

    {
        "case": "empty_name",
        "body": {
            "name": "",
            "code": "TEST"
        },
        "invalid_fields": ["name"]
    },

    {
        "case": "max_name_length_exceeded",
        "body": {
            "name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "code": "TEST"
        },
        "invalid_fields": ["name"]
    },

    {
        "case": "max_code_length_exceeded",
        "body": {
            "name": "TEST",
            "code": "6CHARS",
        },
        "invalid_fields": ["code"]
    },

    {
        "case": "name_already_exists",
        "body": {
            "name": "TEST",
            "code": "CODE"
        },
        "invalid_fields": ["name,code"]
    },

    {
        "case": "code_already_exists",
        "body": {
            "name": "NAME",
            "code": "TEST"
        },
        "invalid_fields": ["name,code"]
    },

    {
        "case": "name_and_code_already_exists",
        "body": {
            "name": "TEST",
            "code": "TEST"
        },
        "invalid_fields": ["name,code"]
    }
]