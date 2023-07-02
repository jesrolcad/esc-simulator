from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.utils.exceptions import BadRequestError, InternalError
from app.routers.schemas.base_schemas import ErrorResponse

async def handle_bad_request_error(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=ErrorResponse(message=exc.message).dict())


async def handle_internal_error(request: Request, exc: InternalError):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ErrorResponse(message=exc.message).dict())