import uvicorn
from fastapi import FastAPI
from app.core.config import Settings
from app.routers.endpoints import data_endpoints
from app.utils.exceptions import BadRequestError, InternalError
from app.routers.exception_handlers import handle_bad_request_error, handle_internal_error

app = FastAPI(title=Settings.PROJECT_NAME, description=Settings.PROJECT_DESCRIPTION, version=Settings.PROJECT_VERSION, docs_url="/")

# Exception handlers
app.add_exception_handler(BadRequestError, handle_bad_request_error)
app.add_exception_handler(InternalError, handle_internal_error)

# Routers
app.include_router(data_endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="localhost", port=8000, reload=True)