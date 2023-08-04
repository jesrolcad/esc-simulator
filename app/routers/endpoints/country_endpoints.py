from fastapi import APIRouter, Depends, status, Response
from app.db.database import get_db 
from app.routers.schemas.api_schemas import ResultResponse
from app.routers.schemas.base_schemas import BaseId
from app.routers.schemas.country_schemas import CountryRequest
from app.routers.endpoints.definitions.country_definitions import get_country_endpoint, get_countries_endpoint, create_country_endpoint, update_country_endpoint
from app.logic.services.country_service import CountryService
from app.routers.api_mappers.country_api_mapper import CountryApiMapper

router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/{country_id}", summary=get_country_endpoint["summary"], description=get_country_endpoint["description"], 
            responses=get_country_endpoint["responses"])
async def get_country(country_id: int, db=Depends(get_db)):
    
    response = CountryService(db).get_country(id=country_id)

    return CountryApiMapper().map_to_country_data_response(response)


@router.get("", summary=get_countries_endpoint["summary"], description=get_countries_endpoint["description"],
            responses=get_countries_endpoint["responses"])
async def get_countries(db=Depends(get_db)):
        
    response = CountryService(db).get_countries()

    return [CountryApiMapper().map_to_country_data_response(country) for country in response]


@router.post("", summary=create_country_endpoint["summary"], description=create_country_endpoint["description"],
            responses=create_country_endpoint["responses"], status_code=status.HTTP_201_CREATED)
async def create_country(country: CountryRequest, db=Depends(get_db)):
        
    country_model = CountryApiMapper().map_to_country_model(country)
    country_response = CountryService(db).create_country(country_model)

    return ResultResponse(message="Country created successfully", data=BaseId(id=country_response.id))


@router.put("/{country_id}", summary=update_country_endpoint["summary"], description=update_country_endpoint["description"],
            responses=update_country_endpoint["responses"], status_code=status.HTTP_204_NO_CONTENT)
async def update_country(country_id: int, country: CountryRequest, db=Depends(get_db)):

    country_model = CountryApiMapper().map_to_country_model(country)
    CountryService(db).update_country(country_id=country_id,country=country_model)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
