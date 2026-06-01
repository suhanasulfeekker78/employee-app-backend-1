"""Employee Repo"""

from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from database import AsyncSession
from exceptions import ConflictException, NotFoundException
from models import Employee, Address, Employee_X_Department, Department

# Manages only db related queries and return exact response


async def create(
    db: AsyncSession,
    name: str,
    email: str,
    age: int | None,
    password_hash: str,
    address_data: dict | None,
) -> Employee:

    db_employee = Employee(name=name, email=email, age=age, password_hash=password_hash)

    db.add(db_employee)

    try:
        await db.flush()
        if address_data:
            db_address = Address(
                line1=address_data.get("line1"),
                city=address_data.get("city"),
                postal_code=address_data.get("postal_code"),
                country=address_data.get("country"),
                employee_id=db_employee.id,
            )
            db.add(db_address)
        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{email.strip()}' is already in use")

    return await find_by_id(db, db_employee.id)  # check


async def search(db: AsyncSession, name: str | None) -> list[Employee]:

    stmt = (
        select(Employee)
        .where(Employee.deleted_at.is_(None))
        .options(selectinload(Employee.addresses), selectinload(Employee.departments))
    )

    if name:
        stmt = stmt.where(Employee.name.ilike(f"%{name}%"))

    results = await db.scalars(stmt)

    return list(results.all())


async def find_all(db: AsyncSession) -> list[Employee]:

    stmt = select(Employee).where(Employee.deleted_at.is_(None))

    results = await db.scalars(stmt)

    return list(results.all())


async def find_by_id(db: AsyncSession, id: int) -> Employee:

    stmt = (
        select(Employee)
        .where(Employee.id == id, Employee.deleted_at.is_(None))
        .options(selectinload(Employee.addresses), selectinload(Employee.departments))
    )
    employee = await db.scalar(stmt)

    if employee:
        employee.addresses = [a for a in employee.addresses if a.deleted_at is None]
        employee.departments = [d for d in employee.departments if d.deleted_at is None]

    return employee


async def update_by_id(db: AsyncSession, id: int, updated_data: dict):

    stmt = (
        update(Employee)
        .where(Employee.id == id, Employee.deleted_at.is_(None))
        .values(**updated_data)
        .returning(Employee)
    )

    try:
        await db.execute(stmt)

        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise ConflictException(
            f"Email '{updated_data.get('email')}' is already in use"
        )

    return await find_by_id(db, id)


async def delete_by_id(db: AsyncSession, id: int) -> Employee:
    employee = await find_by_id(db, id)
    if not employee:
        raise NotFoundException("User target profile missing or already deleted")

    now = datetime.now()
    employee.deleted_at = now

    for address in employee.addresses:
        address.deleted_at = now

    await db.commit()
    return employee


async def get_by_email(db: AsyncSession, email: str) -> Employee | None:
    stmt = select(Employee).where(
        Employee.email == email,
        Employee.deleted_at.is_(None),
    )
    result = await db.scalars(stmt)
    return result.first()


async def add_department_link(
    db: AsyncSession, employee_id: int, department_id: int
) -> None:
    dept_stmt = select(Department).where(
        Department.id == department_id, Department.deleted_at.is_(None)
    )
    if not await db.scalar(dept_stmt):
        raise NotFoundException("department invalid or missing")

    link_stmt = select(Employee_X_Department).where(
        Employee_X_Department.employee_id == employee_id,
        Employee_X_Department.department_id == department_id,
    )
    existing_link = await db.scalar(link_stmt)

    if existing_link:
        if existing_link.deleted_at is not None:
            existing_link.deleted_at = None
            await db.commit()
        return

    junction = Employee_X_Department(
        employee_id=employee_id, department_id=department_id
    )
    db.add(junction)
    await db.commit()


async def remove_department_link(
    db: AsyncSession, employee_id: int, department_id: int
) -> None:
    stmt = select(Employee_X_Department).where(
        Employee_X_Department.employee_id == employee_id,
        Employee_X_Department.department_id == department_id,
        Employee_X_Department.deleted_at.is_(None),
    )
    junction = await db.scalar(stmt)
    if not junction:
        raise NotFoundException("record was not found")

    junction.deleted_at = datetime.now()
    await db.commit()


async def remove_address_link(
    db: AsyncSession, employee_id: int, address_id: int
) -> None:
    stmt = select(Address).where(
        Address.id == address_id,
        Address.employee_id == employee_id,
        Address.deleted_at.is_(None),
    )
    address = await db.scalar(stmt)
    if not address:
        raise NotFoundException("address entry not found")

    address.deleted_at = datetime.now()
    await db.commit()
