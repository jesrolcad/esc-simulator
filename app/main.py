import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.core.config import Settings
from app.routers.endpoints import data_endpoints, song_endpoints
from app.utils.exceptions import BusinessLogicValidationError, InternalError, NotFoundError
from app.routers.exception_handlers import handle_bad_request_error, handle_internal_error, handle_not_found_error, handle_request_validation_error

app = FastAPI(title=Settings.PROJECT_NAME, description=Settings.PROJECT_DESCRIPTION, version=Settings.PROJECT_VERSION, docs_url="/")

# Exception handlers
app.add_exception_handler(BusinessLogicValidationError, handle_bad_request_error)
app.add_exception_handler(InternalError, handle_internal_error)
app.add_exception_handler(NotFoundError, handle_not_found_error)
app.add_exception_handler(RequestValidationError, handle_request_validation_error)

# Routers
app.include_router(data_endpoints.router)
app.include_router(song_endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="localhost", port=8000, reload=True)