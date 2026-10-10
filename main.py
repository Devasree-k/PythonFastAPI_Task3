from fastapi import FastAPI
from fastapi.responses import JSONResponse
from router.driver_router import router as driver_router
from router.collection_router import router as collection_router
from exceptions.app_exceptions import AppError

app = FastAPI(title="Transport Collection Management API", version="1.0.0")

@app.exception_handler(AppError)
async def handle_app_error(request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

app.include_router(driver_router)
app.include_router(collection_router)

@app.get("/")
async def home():
    return {"message": "Transport Collection Management API is running"}
