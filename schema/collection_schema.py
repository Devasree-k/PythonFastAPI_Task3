from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field

class CollectionCreate(BaseModel):
    driver_id: int = Field(gt=0)
    vehicle_number: str = Field(min_length=10, max_length=15)
    collection_date: date
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    evening_collection: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    fuel_expense: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    other_expense: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

class CollectionUpdate(BaseModel):
    driver_id: int = Field(gt=0)
    vehicle_number: str = Field(min_length=10, max_length=15)
    collection_date: date
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    evening_collection: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    fuel_expense: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    other_expense: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    

class CollectionResponse(BaseModel):
    id: int
    driver_id: int
    driver_name: str
    vehicle_number: str
    collection_date: date
    morning_trips: int
    evening_trips: int
    morning_collection: Decimal
    evening_collection: Decimal
    fuel_expense: Decimal
    other_expense: Decimal
    total_trips: int
    total_collection: Decimal
    total_expense: Decimal
    net_collection: Decimal
    report_file_path: str | None = None
    created_at: datetime

class CollectionPage(BaseModel):
    items: list[CollectionResponse]
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool

