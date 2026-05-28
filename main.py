import logging
from fastapi import FastAPI

from contextlib import asynccontextmanager
from middleware import configure_middleware

from database import create_tables
from routers.employee_router import router as employee_router
from config import APP_ENV

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="info.log"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(
    title="Employee CRUD API", 
    description="Simple Employee API with dict storage ", 
    version="1.0.0",
    lifespan=lifespan
)

configure_middleware(app)

app.include_router(employee_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "message": "Employee CRUD API is running", "environment": APP_ENV}

