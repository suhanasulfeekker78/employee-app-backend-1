
from datetime import datetime

from fastapi import status
from exceptions import ConflictException, NotFoundException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from models.department import Department
from models.employee_x_department import Employee_X_Department
from models.employee import Employee
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

    stmt = select(Department).where(Department.deleted_at.is_(None))
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def find_by_id(db: AsyncSession, id: int) -> Department | None:
    stmt = (
        select(Department)
        .where(Department.id == id, Department.deleted_at.is_(None))
        .options(selectinload(Department.employees))
    )
    department = await db.scalar(stmt)

    if department:
        department.employees = [emp for emp in department.employees if emp.deleted_at is None]
        
    return department

async def update_by_id(db: AsyncSession, id, data: dict) -> Department:

    stmt = update(Department).where(Department.id == id, Department.deleted_at.is_(None)).values(**data).returning(Department)

    try: 
        updated_department = (await db.execute(stmt)).scalar_one()
        await db.commit()

    except IntegrityError:
        raise ConflictException(f"{data.get("name") or "department"} already exist")
    except NoResultFound:
        raise NotFoundException("department not found")
    
    return updated_department

async def delete_by_id(db: AsyncSession, id: int) -> Department:
    now = datetime.now()
    stmt = (
        update(Department)
        .where(Department.id == id, Department.deleted_at.is_(None))
        .values(deleted_at=now)
        .returning(Department)
    )
    try:
        result = await db.execute(stmt)
        updated_department = result.scalar_one()

        junction_stmt = (
            update(Employee_X_Department)
            .where(Employee_X_Department.department_id == id, Employee_X_Department.deleted_at.is_(None))
            .values(deleted_at=now)
        )
        await db.execute(junction_stmt)
        
        await db.commit()
    except NoResultFound:
        await db.rollback()
        raise NotFoundException("Department not found or already deleted")
        
    return updated_department