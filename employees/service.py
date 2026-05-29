""" Employee Service"""

from fastapi import status

from database import AsyncSession
from models.employee import Employee
from employees.repo import create, search, find_all, find_by_id, update_by_id, delete_by_id
from exceptions import BadRequestException, NotFoundException
from employees.schemas import CreateEmployeeRequest
from auth.utils import hash_password

# Mainly manage business logics


async def create_employee(db: AsyncSession, data: CreateEmployeeRequest) -> Employee:
    hashed=hash_password(data.pswd)
    # employee:dict={
    #     name:data.name,
    #     email:data.email,
    #     age:data.age,
    #     password_hash:hashed
    # }
    employee = await create(db, data.name, data.email, data.age, password_hash=hashed)

    return employee

async def list_employee(db: AsyncSession) -> list[Employee]:
    return await find_all(db)

async def search_employee(db: AsyncSession, name: str) -> list[Employee]:

    if name is not None:
        name = name.strip()
    
    return await search(db, name)


async def employee_by_id(db: AsyncSession, id: int) -> Employee:
    
    employee = await find_by_id(db, id)

    if employee is None:
        raise NotFoundException("employee not found")
    
    return employee

async def update_employee(db: AsyncSession, id: int, updated_data: dict) -> Employee:

    updated_fields = {}

    if updated_data.get("name") is not None:
        if not isinstance(updated_data.get("name"), str):
            raise BadRequestException("name must be a non-empty string")
        
        updated_fields["name"] = updated_data.get("name")
    
    if updated_data.get("email") is not None:
        if not isinstance(updated_data.get("email"), str):
            raise BadRequestException("email must be a non-empty string")
        
        updated_fields["email"] = updated_data.get("email")

    updated_employee = await update_by_id(db, id, updated_data=updated_fields)

    return updated_employee


async def delete_employee(db: AsyncSession, id: int):
    return await delete_by_id(db, id)