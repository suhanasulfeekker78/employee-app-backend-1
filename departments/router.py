
from fastapi import APIRouter, Depends, Body, status

from database import AsyncSession, get_db
from departments import service as department_service
router = APIRouter(prefix="/department", tags=["Departments"])



@router.post("", status_code=status.HTTP_201_CREATED)
async def create_department(data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    return (await department_service.create_department(db, data)).to_api_dict()

@router.put("/{id}")
async def update_department(id: int, data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    return (await department_service.update_department(db, id, data)).to_api_dict()

@router.get("")
async def list_all_department(db: AsyncSession = Depends(get_db)):
    return [ dept.to_api_dict() for dept in (await department_service.list_all_department(db))]

@router.post("/{id}/{employee_id}")
async def add_employee( id: int, employee_id: int, db: AsyncSession = Depends(get_db)):
    return await department_service.add_employee_to_department(db, id, employee_id)

@router.delete("/{id}/{employee_id}")
async def remove_employee( id: int, employee_id: int, db: AsyncSession = Depends(get_db)):
    return await department_service.remove_employee_to_department(db, id, employee_id)

