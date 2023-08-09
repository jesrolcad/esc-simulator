from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.exceptions import BusinessLogicValidationError, InternalError, NotFoundError
from app.routers.schemas.api_schemas import ErrorDetailResponse, ErrorResponse

async def handle_bad_request_error(request: Request, exc: BusinessLogicValidationError):
    error_detail_response = ErrorDetailResponse(field=exc.field, message=exc.message)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=ErrorResponse(errors=[error_detail_response]).model_dump())

async def handle_not_found_error(request: Request, exc: NotFoundError):
    error_detail_response = ErrorDetailResponse(field=exc.field,message=exc.message)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=ErrorResponse(errors=[error_detail_response]).model_dump())

async def handle_internal_error(request: Request, exc: InternalError):
    error_detail_response = ErrorDetailResponse(message=exc.message)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ErrorResponse(errors=[error_detail_response]).model_dump())

async def handle_request_validation_error(request: Request, exc: RequestValidationError):
    error_response = ErrorResponse()
    for error in exc.errors():
        error_loc_length = len(error["loc"])
        if error_loc_length == 1:
            field = error["loc"][0]
            message = "body required"
        else:
            field = error["loc"][1]
            message = error["msg"]
        error_detail_response = ErrorDetailResponse(field=field, message=message)
        error_response.errors.append(error_detail_response)

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_response.model_dump())
