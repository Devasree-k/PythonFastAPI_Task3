from psycopg.errors import UniqueViolation
from exceptions.app_exceptions import NotFoundError, ConflictError
from repositories.driver_repository import DriverRepository

class DriverService:
    def __init__(self):
        self.repository = DriverRepository()

    async def create(self, data: dict):
        try:
            return await self.repository.create(data)
        except UniqueViolation:
            raise ConflictError("A driver with this phone number already exists")


    async def get_all(self):
        return await self.repository.get_all()


    async def get_by_id(self, driver_id: int):
        driver = await self.repository.get_by_id(driver_id)
        
        if not driver:
            raise NotFoundError("Driver not found")
        return driver


    async def update(self, driver_id: int, data: dict):
        try:
            driver = await self.repository.update(driver_id, data)
        except UniqueViolation:
            raise ConflictError("A driver with this phone number already exists")
        
        if not driver:
            raise NotFoundError("Driver not found")
        return driver


    async def delete(self, driver_id: int):
        result = await self.repository.delete(driver_id)

        if not result:
            raise NotFoundError("Driver not found")

        return {"message": "Driver deleted successfully"}
