import logging
from datetime import date

from fastapi import FastAPI, status, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

from contextlib import asynccontextmanager
from middleware.logger import RequestLoggingMiddleware
from sqlalchemy.sql import select, update
from sqlalchemy.exc import IntegrityError

from database import create_tables, AsyncSession, get_db
from models import Employee


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

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/", tags={"Root"})
def hello():
    return {"message": "Hello world"}


@app.post("/employee", status_code=status.HTTP_201_CREATED, tags=["Employees"])
async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    name = body.get("name")
    email = body.get("email")
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
    
    db_employee = Employee(name=name.strip(), email=email.strip())

    db.add(db_employee)
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
    await db.refresh(db_employee)

    return db_employee.to_api_dict()

@app.get("/employee", status_code=status.HTTP_200_OK, tags=["Employees"])
async def list_employee(db: AsyncSession = Depends(get_db)):

    stnt = select(Employee).where(Employee.deleted_at.is_(None))
    results = await db.scalars(stnt)

    return [r.to_api_dict() for r in results]

    

@app.get("/employee/{id}", tags=["Employees"])
async def single_employee(id: int, db: AsyncSession = Depends(get_db)):


    stnt = select(Employee).where(Employee.id == id, Employee.deleted_at.is_(None))

    result = await db.scalar(stnt)

    return result.to_api_dict() if result is not None else None

@app.put("/employee/{id}", tags=["Employees"])
async def update_employee(id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db)):


    updated_fields = {}

    if body.get("name") is not None:
        if not isinstance(body.get("name"), str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
        
        updated_fields["name"] = body.get("name")
    
    if body.get("email") is not None:
        if not isinstance(body.get("email"), str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
        
        updated_fields["email"] = body.get("email")
        

    stnt = update(Employee).where(Employee.id == id).values(**updated_fields).returning(Employee)

    try:
        result = await db.execute(stnt)

        updated_employee = result.scalar()

        if update_employee is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")
        
        await db.commit()

        return updated_employee.to_api_dict()
    except IntegrityError:
        await db.rollback()

    
@app.delete("/employee/{id}", tags=["Employees"])
async def delete_employee(id: int, db: AsyncSession = Depends(get_db)):


    stnt = update(Employee).where(Employee.id == id).values(deleted_at=date.today())

    try:
        await db.execute(stnt)
        await db.commit()
        
    except IntegrityError:
        await db.rollback()


