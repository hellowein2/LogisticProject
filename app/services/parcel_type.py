from app.repositories.parcel_type import ParcelTypeRepository
from app.schemas.parcels import ParcelTypeOut


class ParcelTypeService:
    def __init__(self, repo: ParcelTypeRepository):
        self.repo = repo

    async def list_parcel_types(self) -> list[ParcelTypeOut]:
        parcel_types = await self.repo.list()
        return [ParcelTypeOut.model_validate(pt) for pt in parcel_types]
