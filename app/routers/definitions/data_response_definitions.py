from fastapi import status
from app.routers.schemas.base_schemas import ResultResponse, ErrorResponse


populate_data_responses = {
    status.OK: {
        "model": ResultResponse, 
        "description": "Data populated successfully"},

    status.BAD_REQUEST: {
        "model": ErrorResponse, 
        "description": "Bad request"}}