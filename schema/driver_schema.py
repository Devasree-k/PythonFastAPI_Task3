from pydantic import BaseModel, Field

class DriverCreate(BaseModel):
    driver_name: str = Field(min_length=2, max_length=100)
    phone_number: str = Field(pattern="^[6-9][0-9]{9}$")
    is_active: bool = True

class DriverUpdate(BaseModel):
    driver_name: str | None = Field(default=None, min_length=2, max_length=100)
    phone_number: str | None = Field(pattern="^[6-9][0-9]{9}$")
    is_active: bool | None = None


class DriverResponse(BaseModel):
    driver_id: int
    driver_name: str
    phone_number: str
    is_active: bool

