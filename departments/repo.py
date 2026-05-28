from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, update
from models.department import Department

from database import AsyncSession


async def create(db: AsyncSession, data: dict) -> Department:

    department = Department(**data)
    
    db.add(department)

    try:
        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f"{data.get("name")} already exist")
    
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
        raise HTTPException(status.HTTP_409_CONFLICT, detail={f"{data.get("name") or "department"} already exist"})
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={f"department not found"})
    
    return updated_department
