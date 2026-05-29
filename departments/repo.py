
from datetime import datetime

from fastapi import status
from exceptions import ConflictException, NotFoundException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, update
from models.department import Department
from models.employee_x_department import Employee_X_Department

from database import AsyncSession


async def create(db: AsyncSession, data: dict) -> Department:

    department = Department(**data)
    
    db.add(department)

    try:
        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"{data.get("name")} already exist")
    
    await db.refresh(department)

    return department 

async def find_all(db: AsyncSession) -> list[Department]:

    stnt = select(Department).where(Department.deleted_at.is_(None))

    return (await db.execute(stnt)).scalars()

async def update_by_id(db: AsyncSession, id, data: dict) -> Department:

    stnt = update(Department).where(Department.id == id, Department.deleted_at.is_(None)).values(**data).returning(Department)

    try: 
        updated_department = (await db.execute(stnt)).scalar_one()
        await db.commit()

    except IntegrityError:
        raise ConflictException(f"{data.get("name") or "department"} already exist")
    except NoResultFound:
        raise NotFoundException("department not found")
    
    return updated_department

async def insert_employee_to_department(db: AsyncSession, id: int, employee_id: int) -> Employee_X_Department:

    employee_x_department = Employee_X_Department(department_id=id, employee_id=employee_id)

    db.add(employee_x_department)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("employee already exist in the department")
    
    await db.refresh(employee_x_department)
    return employee_x_department

async def delete_employee_from_department(db: AsyncSession, id: int, employee_id: int) -> Employee_X_Department:

    stnt = update(Employee_X_Department).where(Employee_X_Department.department_id == id, Employee_X_Department.employee_id== employee_id, Employee_X_Department.deleted_at.is_(None)).values(deleted_at=datetime.now()).returning(Employee_X_Department)

    try:
        updated_employee_x_department = (await db.execute(stnt)).scalar_one()
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("employee already exist in the department")
    except NoResultFound:
        raise NotFoundException("employee to department record not found")
    
    return updated_employee_x_department