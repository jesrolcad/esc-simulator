from fastapi import APIRouter, Depends, status, Response
from app.db.database import get_db 
from app.routers.schemas.api_schemas import ResultResponse
from app.routers.schemas.base_schemas import BaseId
from app.routers.schemas.country_schemas import CountryRequest
from app.routers.endpoints.definitions import country_definitions as defs
from app.logic.services.country_service import CountryService
from app.routers.api_mappers.country_api_mapper import CountryApiMapper

router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/{country_id}", summary=defs.get_country_endpoint["summary"], description=defs.get_country_endpoint["description"], 
            responses=defs.get_country_endpoint["responses"])
async def get_country(country_id: int, db=Depends(get_db)):
    
    response = CountryService(db).get_country(id=country_id)

    return CountryApiMapper().map_to_country_data_response(response)


@router.get("", summary=defs.get_countries_endpoint["summary"], description=defs.get_countries_endpoint["description"],
            responses=defs.get_countries_endpoint["responses"])
async def get_countries(db=Depends(get_db)):
        
    response = CountryService(db).get_countries()

    return [CountryApiMapper().map_to_country_data_response(country) for country in response]


@router.post("", summary=defs.create_country_endpoint["summary"], description=defs.create_country_endpoint["description"],
            responses=defs.create_country_endpoint["responses"], status_code=status.HTTP_201_CREATED)
async def create_country(country: CountryRequest, db=Depends(get_db)):
        
    country_model = CountryApiMapper().map_to_country_model(country)
    country_response = CountryService(db).create_country(country_model)

    return ResultResponse(message="Country created successfully", data=BaseId(id=country_response.id))


@router.put("/{country_id}", summary=defs.update_country_endpoint["summary"], description=defs.update_country_endpoint["description"],
            responses=defs.update_country_endpoint["responses"], status_code=status.HTTP_204_NO_CONTENT)
async def update_country(country_id: int, country: CountryRequest, db=Depends(get_db)):

    country_model = CountryApiMapper().map_to_country_model(country)
    CountryService(db).update_country(country_id=country_id,country=country_model)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{country_id}", summary=defs.delete_country_endpoint["summary"], description=defs.delete_country_endpoint["description"],
            responses=defs.delete_country_endpoint["responses"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(country_id: int, db=Depends(get_db)):

    CountryService(db).delete_country(country_id=country_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
