import pytest
from uuid import UUID, uuid4
from app.adapters.repositories.base_repository import BaseRepository, T


def test__base_repository_is_abstract():
	with pytest.raises(TypeError, match="Can't instantiate abstract class"):
		BaseRepository()


class TestBaseRepositoryImpl(BaseRepository):
	async def get_by_id(self, _id: int) -> T:
		await super().get_by_id(_id)

	async def get_by_uuid(self, uuid: UUID) -> T:
		await super().get_by_uuid(uuid)


@pytest.mark.asyncio
async def test__get_by_id_raise_error_when_not_implemented():
	repo = TestBaseRepositoryImpl()

	assert isinstance(repo, TestBaseRepositoryImpl)
	with pytest.raises(NotImplementedError):
		await repo.get_by_id(_id=1)


@pytest.mark.asyncio
async def test__get_by_uuid_raise_error_when_not_implemented():
	repo = TestBaseRepositoryImpl()

	assert isinstance(repo, TestBaseRepositoryImpl)
	with pytest.raises(NotImplementedError):
		await repo.get_by_uuid(uuid=uuid4())
