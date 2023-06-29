from fastapi import APIRouter, Depends
from app.routers.schemas.base_schemas import ResultResponse
from app.routers.schemas.data_schemas import YearRequest
from app.logic.services.data_service import DataService
from app.routers.definitions.data_response_definitions import populate_data_responses
from app.db.database import get_db 

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/populate", name="populate_data", responses=populate_data_responses)
async def populate_data(year_request: YearRequest, db: get_db = Depends()):
    DataService(db).scrape_data(year_request.years)
    return ResultResponse(result=True, message="Data populated successfully")
