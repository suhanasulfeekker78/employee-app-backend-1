import logging
from fastapi import FastAPI

from contextlib import asynccontextmanager
from middleware import configure_middleware

from employees.router import router as employee_router
from departments.router import router as department_router
from exceptions.handler import register_exception_handlers
from auth.router import router as auth_router

from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Employee CRUD API",
    description="Simple Employee API with dict storage ",
    version="1.0.0",
    lifespan=lifespan,
)

configure_middleware(app)

register_exception_handlers(app)

app.include_router(employee_router)
app.include_router(department_router)
app.include_router(auth_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "Employee CRUD API is running",
        "environment": settings.app_env,
    }
