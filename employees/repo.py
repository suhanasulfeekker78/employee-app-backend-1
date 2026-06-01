"""Employee Repo"""

from datetime import datetime

from fastapi import status
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, update

from database import AsyncSession
from exceptions import ConflictException, NotFoundException
from models.employee import Employee

# Manages only db related queries and return exact response


async def create(db: AsyncSession, name: str, email: str, age:int|None, password_hash:str) -> Employee:

    db_employee = Employee(name=name, email=email, age=age, password_hash=password_hash)

    db.add(db_employee)

    try:
        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{email.strip()}' is already in use")
        

    await db.refresh(db_employee)

    return db_employee

async def search(db: AsyncSession, name: str | None) -> list[Employee]:
    
    stnt = select(Employee).where(Employee.deleted_at.is_(None))

    if name is not None and name:
        stnt = stnt.where(Employee.name.ilike(f"%{name}%"))

    results = await db.scalars(stnt)

    return results

async def find_all(db: AsyncSession) -> list[Employee]:
    
    stnt = select(Employee).where(Employee.deleted_at.is_(None))

    results = await db.scalars(stnt)

    return results

async def find_by_id(db: AsyncSession, id: int) -> Employee:
    
    stnt = select(Employee).where(Employee.id == id,Employee.deleted_at.is_(None))

    employee = await db.scalar(stnt)

    return employee


async def update_by_id(db: AsyncSession, id: int, updated_data: dict):

    stnt = update(Employee).where(Employee.id == id, Employee.deleted_at.is_(None)).values(**updated_data).returning(Employee)

    updated_employee = None
    try:

        result  = (await db.execute(stnt))
        updated_employee = result.scalar_one()

        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{updated_data.get("email")}' is already in use")
    except NoResultFound:
        raise NotFoundException("user not found")
    return updated_employee

async def delete_by_id(db: AsyncSession, id: int):

    stnt = update(Employee).where(Employee.id == id, Employee.deleted_at.is_(None)).values(deleted_at=datetime.now()).returning(Employee)

    try:
        result = await db.execute(stnt)
        updated_employee  = result.scalar_one()
        
        await db.commit()

    except NoResultFound:
        raise NotFoundException("user not found or has already deleted")
    
    return updated_employee

async  def get_by_email(db: AsyncSession, email:str)->Employee|None:
    stmt= select(Employee).where( Employee.email==email,Employee.deleted_at.is_(None),)
    result=await db.scalars(stmt)
    return result.first()
