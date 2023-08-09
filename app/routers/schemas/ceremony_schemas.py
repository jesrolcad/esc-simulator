from app.routers.schemas.base_schemas import BaseId, BaseCeremonyType, BaseCeremony
from app.routers.schemas.common_schemas import EventWithoutCeremoniesDataResponse


class CeremonyTypeDataResponse(BaseCeremonyType, BaseId):
    pass


class CeremonyDataResponse(BaseCeremony, BaseId):
    ceremony_type: CeremonyTypeDataResponse
    event: EventWithoutCeremoniesDataResponse





