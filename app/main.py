import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from app.core.config import BaseSettings as Settings
from app.routers.endpoints import data_endpoints, song_endpoints, country_endpoints, event_endpoints, simulator_endpoints
from app.utils.exceptions import BusinessLogicValidationError, InternalError, NotFoundError
from app.routers.exception_handlers import handle_bad_request_error, handle_internal_error, handle_not_found_error, handle_request_validation_error

app = FastAPI(title=Settings.PROJECT_NAME, description=Settings.PROJECT_DESCRIPTION, version=Settings.PROJECT_VERSION, docs_url="/")

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema

app.openapi = custom_openapi

# Exception handlers
app.add_exception_handler(BusinessLogicValidationError, handle_bad_request_error)
app.add_exception_handler(InternalError, handle_internal_error)
app.add_exception_handler(NotFoundError, handle_not_found_error)
app.add_exception_handler(RequestValidationError, handle_request_validation_error)

# Routers
app.include_router(data_endpoints.router)
app.include_router(song_endpoints.router)
app.include_router(country_endpoints.router)
app.include_router(event_endpoints.router)
app.include_router(simulator_endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="localhost", port=8000, reload=True)