# Delivery controller
from src.modules.cyc.delivery import service
from src.core.deps import DataBaseDep

async def get_deliveries_controller(db: DataBaseDep):
  return await service.get_deliveries_service(db)
