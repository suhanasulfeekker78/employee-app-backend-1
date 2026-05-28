""" Employee Service"""

from fastapi import status
from fastapi.exceptions import HTTPException

from database import AsyncSession
from models.employee import Employee
from repositories.employee_repo import create, find_all, find_by_id, update_by_id, delete_by_id

# Mainly manage business logics


async def create_employee(db: AsyncSession, name: str, email: str) -> Employee:

    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
    
    employee = await create(db, name, email)

    return employee

async def list_employee(db: AsyncSession) -> list[Employee]:
    return await find_all(db)

async def employee_by_id(db: AsyncSession, id: int) -> Employee:
    
    employee = await find_by_id(db, id)

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="employee not found")
    
    return employee

async def update_employee(db: AsyncSession, id: int, updated_data: dict) -> Employee:

    updated_fields = {}

    if updated_data.get("name") is not None:
        if not isinstance(updated_data.get("name"), str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
        
        updated_fields["name"] = updated_data.get("name")
    
    if updated_data.get("email") is not None:
        if not isinstance(updated_data.get("email"), str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
        
        updated_fields["email"] = updated_data.get("email")

    updated_employee = await update_by_id(db, id, updated_data=updated_fields)

    return updated_employee


async def delete_employee(db: AsyncSession, id: int):
    return await delete_by_id(db, id)