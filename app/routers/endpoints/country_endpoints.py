from fastapi import APIRouter, Depends
from app.db.database import get_db 
from app.routers.endpoints.definitions.country_definitions import get_country_endpoint
from app.logic.services.country_service import CountryService
from app.routers.api_mappers.country_api_mapper import CountryApiMapper

router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/{country_id}", summary=get_country_endpoint["summary"], description=get_country_endpoint["description"], 
            response_model=get_country_endpoint["responses"], responses=get_country_endpoint["responses"])
async def get_country(country_id: int, db=Depends(get_db)):
    
    response = CountryService(db).get_country(id=country_id)
    return CountryApiMapper().map_to_country_data_response(response)