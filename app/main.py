import uvicorn
import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from app.core.config import BaseSettings as Settings
from app.db.database import get_db
from app.routers.endpoints import data_endpoints, song_endpoints, country_endpoints, event_endpoints, simulator_endpoints
from app.routers.operations.country_operations import CountryMutation, CountryQuery
from app.routers.operations.event_operations import EventMutation, EventQuery
from app.routers.operations.song_operations import SongQuery, SongMutation
from app.routers.operations.simulation_operations import SimulatorQuery, SimulatorMutation
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

# REST Exception handlers
app.add_exception_handler(BusinessLogicValidationError, handle_bad_request_error)
app.add_exception_handler(InternalError, handle_internal_error)
app.add_exception_handler(NotFoundError, handle_not_found_error)
app.add_exception_handler(RequestValidationError, handle_request_validation_error)

# REST Routers
app.include_router(data_endpoints.router)
app.include_router(song_endpoints.router)
app.include_router(country_endpoints.router)
app.include_router(event_endpoints.router)
app.include_router(simulator_endpoints.router)

# GraphQL Router
# create Query class, which extends from another query classes (song, country, event...)
# Example:
@strawberry.type
class Query(SongQuery, CountryQuery, EventQuery, SimulatorQuery):
    pass

@strawberry.type
class Mutation(SongMutation, CountryMutation, EventMutation, SimulatorMutation):
    pass

# GraphQL Custom Context
class CustomContext(BaseContext):
    def __init__(self, db):
        super().__init__()
        self.db = db

async def get_context(db: Session = Depends(get_db)) -> CustomContext:
    return CustomContext(db=db)


schema = strawberry.Schema(Query, Mutation)

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="localhost", port=8000, reload=True)