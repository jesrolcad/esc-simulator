from fastapi import status
from app.routers.schemas.base_schemas import ResultResponse, ErrorResponse

post_populate = {
    "summary": "Populate ESC data",
    "description": """Populate events, countries and songs for the given years. If the year is not provided, no data will be populated. 
                    If the year has already been populated, it will be skipped.""",
    "responses": {
        status.HTTP_200_OK: {
            "model": ResultResponse, 
            "description": "Data populated successfully"},

        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse, 
            "description": "Bad request"}}
}