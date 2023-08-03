from fastapi import status
from app.routers.schemas.country_schemas import CountryDataResponse
from app.routers.schemas.api_schemas import ErrorResponse, ResultResponse

get_country_endpoint = {
    "summary": "Get country by id",
    "description": "Get country by id. If  the country is not found, a 404 response will be returned",
    "responses": {
        status.HTTP_200_OK: {
            "model": CountryDataResponse,
            "description": "Country details retrieved successfully"
    },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Country not found"
        }
    }
}


get_countries_endpoint = {
    "summary": "Get all countries",
    "description": "Get all countries. If no countries are found, an empty list will be returned",
    "responses": {
        status.HTTP_200_OK: {
            "model": list[CountryDataResponse],
            "description": "Countries retrieved successfully"
        }
    }
}

create_country_endpoint = {
    "summary": "Create country",
    "description": "Create a new country. If the country is created successfully, the country id will be returned",
    "responses": {
        status.HTTP_201_CREATED: {
            "model": ResultResponse,
            "description": "Country created successfully"
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid request body"
        }
    }
}
