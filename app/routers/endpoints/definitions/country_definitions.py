from fastapi import status
from app.routers.schemas.country_schemas import CountryDataResponse
from app.routers.schemas.api_schemas import ErrorResponse

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