from fastapi import Request
from app.main import app
from app.utils.exceptions import BadRequestError
from app.routers.schemas.base_schemas import ErrorResponse

@app.exception_handler(BadRequestError)
async def handle_bad_request_error(request: Request, exc: BadRequestError):
    return ErrorResponse(message=exc.message)

