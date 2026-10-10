from fastapi import APIRouter, status, HTTPException
from schema.driver_schema import DriverCreate, DriverUpdate, DriverResponse 
from services.driver_service import DriverService

router = APIRouter(prefix="/drivers", tags=["Drivers"])
service = DriverService()

@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(data: DriverCreate):
    return await service.create(data.model_dump())

@router.get("/", response_model=list[DriverResponse])
async def get_drivers():
    return await service.get_all()

@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(driver_id: int):
    return await service.get_by_id(driver_id)

@router.put("/{driver_id}", response_model=DriverResponse)
async def replace_driver(driver_id: int, data: DriverUpdate):
    return await service.update(driver_id, data.model_dump())



@router.patch("/{driver_id}")
async def update_driver(
    driver_id: int,
    driver: DriverUpdate
):
    update_data = driver.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update"
        )

    return await service.update( driver_id, update_data )


@router.delete("/{driver_id}")
async def delete_driver(driver_id: int):
    return await service.delete(driver_id)
