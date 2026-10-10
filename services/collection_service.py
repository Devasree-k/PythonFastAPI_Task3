from pathlib import Path
from uuid import uuid4
import aiofiles
from fastapi import UploadFile
from config import settings
from exceptions.app_exceptions import NotFoundError, AppError
from models.collection_model import CollectionTotals
from repositories.collection_repository import CollectionRepository
from repositories.driver_repository import DriverRepository

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

class CollectionService:
    def __init__(self):
        self.repository = CollectionRepository()
        self.driver_repository = DriverRepository()

    
    def calculate_totals(self, data: dict) -> CollectionTotals:

        total_trips = data["morning_trips"] + data["evening_trips"]

        total_collection = data["morning_collection"] + data["evening_collection"]

        total_expense = data["fuel_expense"] + data["other_expense"]

        return CollectionTotals(total_trips, 
                                total_collection, 
                                total_expense, 
                                total_collection - total_expense)

    async def create(self, data: dict):
        if not await self.driver_repository.get_by_id(data["driver_id"]):
            raise NotFoundError("Driver not found")
        return await self.repository.create(data, self.calculate_totals(data))


    async def get_by_id(self, collection_id: int):
        item = await self.repository.get_by_id(collection_id)
        if not item:
            raise NotFoundError("Collection record not found")
        return item


    async def get_page(self, page: int, page_size: int, driver_id: int | None):
        items, total = await self.repository.get_page(page, page_size, driver_id)
        pages = (total + page_size - 1) // page_size
        return {"items": items, "page": page, "page_size": page_size, "total": total,
                "total_pages": pages, "has_next": page < pages, "has_previous": page > 1}


    async def update(self, collection_id: int, data: dict):
        await self.get_by_id(collection_id)
        if not await self.driver_repository.get_by_id(data["driver_id"]):
            raise NotFoundError("Driver not found")
        return await self.repository.update(collection_id, data, self.calculate_totals(data))


    async def delete(self, collection_id: int):
        if not await self.repository.delete(collection_id):
            raise NotFoundError("Collection record not found")
        return {"message": "Collection record deleted successfully"}


    async def upload_report(self, collection_id: int, file: UploadFile):
        await self.get_by_id(collection_id)
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            await file.close()
            raise AppError("Only PDF, JPG, JPEG and PNG files are allowed", 415)
        settings.upload_dir.mkdir(parents=True, exist_ok=True)
        saved_path = settings.upload_dir / f"{uuid4().hex}{suffix}"
        size = 0
        try:
            async with aiofiles.open(saved_path, "wb") as output:
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    if size > settings.max_upload_size:
                        raise AppError("File is too large. Maximum size is 5 MB", 413)
                    await output.write(chunk)

            if not await self.repository.update_report_path(collection_id, str(saved_path)):
                raise NotFoundError("Collection record not found")
            return {"message": "Report uploaded successfully", "file_path": str(saved_path)}
        except Exception:
            if saved_path.exists():
                saved_path.unlink()
            raise
        finally:
            await file.close()
