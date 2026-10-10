from fastapi import APIRouter, File, Query, UploadFile, status
from schema.collection_schema import CollectionCreate, CollectionUpdate, CollectionResponse, CollectionPage
from services.collection_service import CollectionService

router = APIRouter(prefix="/collections", tags=["Transport Collections"])
service = CollectionService()

@router.post("/", 
            response_model=CollectionResponse, 
            status_code=status.HTTP_201_CREATED
            )
async def create_collection(data: CollectionCreate):
    return await service.create(data.model_dump())


@router.get("/", response_model=CollectionPage)
async def get_collections(page: int = Query(1, ge=1), 
                          page_size: int = Query(10, ge=1, le=100),
                          driver_id: int | None = Query(None, gt=0)
                          ):
    return await service.get_page(page, page_size, driver_id)


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(collection_id: int):
    return await service.get_by_id(collection_id)


@router.put("/{collection_id}", response_model=CollectionResponse)
async def update_collection(collection_id: int, data: CollectionUpdate):
    return await service.update(collection_id, data.model_dump())


@router.delete("/{collection_id}")
async def delete_collection(collection_id: int):
    return await service.delete(collection_id)


@router.post("/{collection_id}/report")
async def upload_collection_report(collection_id: int, file: UploadFile = File(...)):
    return await service.upload_report(collection_id, file)
