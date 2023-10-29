from app.routers.schemas.base_schemas import BaseId, BaseCeremony
from app.routers.schemas.common_schemas import EventWithoutCeremoniesDataResponse, CeremonyTypeDataResponse


class CeremonyDataResponse(BaseCeremony, BaseId):
    ceremony_type: CeremonyTypeDataResponse
    event: EventWithoutCeremoniesDataResponse






