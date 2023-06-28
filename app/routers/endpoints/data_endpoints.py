from fastapi import APIRouter, Depends
from app.routers.schemas.base_response_schemas import ResultResponse
from app.logic.services.data_service import DataService
from app.db.database import get_db 

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/populate", response_model=ResultResponse)
async def populate_data(years: list[int], db: get_db = Depends()):
    return ResultResponse(result=True, message="Data populated successfully")
