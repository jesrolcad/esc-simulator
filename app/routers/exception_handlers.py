from fastapi import Request
from fastapi.responses import JSONResponse
from app.main import app
from app.utils.exceptions import BadRequestError, InternalError
from app.routers.schemas.base_schemas import ErrorResponse


@app.exception_handler(BadRequestError)
async def handle_bad_request_error(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=400, content=ErrorResponse(message=exc.message).dict())


@app.exception_handler(InternalError)
async def handle_internal_error(request: Request, exc: InternalError):
    return JSONResponse(status_code=500, content=ErrorResponse(message=exc.message).dict())