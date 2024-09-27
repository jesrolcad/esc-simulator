import strawberry

from app.logic.services.simulator_service import SimulatorService
from app.routers.schemas.api_schemas import ResultResponseQL

@strawberry.type
class SimulatorMutation:
    @strawberry.mutation
    def create_event_simulation(self, info: strawberry.Info, event_id: int)-> ResultResponseQL:
        SimulatorService(info.context.db).create_simulation(event_id=event_id)

        return ResultResponseQL(success=True,message="Event simulated successfully")

    @strawberry.mutation
    def delete_event_simulation(self, info: strawberry.Info, event_id: int)-> ResultResponseQL:
        SimulatorService(info.context.db).delete_simulation_by_event_id(event_id=event_id)

        return ResultResponseQL(success=True,message="Event simulation deleted successfully")