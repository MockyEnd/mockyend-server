from app.adapters.repositories.operation_repository import OperationRepository
from app.adapters.repositories.schemas import OperationCreate
from app.domain.models.operation import Operation


class CreateOperationService:
	def __init__(self, repository: OperationRepository):
		self.repository = repository

	async def create(self, operation_create: OperationCreate) -> Operation:
		return await self.repository.save(operation=operation_create)
