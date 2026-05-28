"""Employee Router"""

from fastapi import APIRouter, Body, status, Depends

from database import AsyncSession, get_db

from employees import service

# Contains mainly the routes , parsing logics 

router = APIRouter(prefix="/employee", tags=["Employees"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):

    name = body.get("name")
    email = body.get("email")

    employee = await service.create_employee(db, name, email)

    return employee.to_api_dict()


@router.get("/search")
async def search_employee(name: str = "", db: AsyncSession = Depends(get_db)):

    employees = await service.search_employee(db, name)

    return [r.to_api_dict() for r in employees]


@router.get("")
async def list_employee(db: AsyncSession = Depends(get_db)):

    employees = await service.list_employee(db)

    return [r.to_api_dict() for r in employees]


@router.get("/{id}")
async def get_employee_by_id(id: int, db: AsyncSession = Depends(get_db)):

    employee = await service.employee_by_id(db, id)

    return employee.to_api_dict()

@router.put("/{id}")
async def update_employee(id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db)):

    updated_employee = await service.update_employee(db, id, body)

    return updated_employee.to_api_dict()

@router.delete("/{id}")
async def delete_employee(id: int, db: AsyncSession = Depends(get_db)):

    employee = await service.delete_employee(db, id)

    return employee.to_api_dict()