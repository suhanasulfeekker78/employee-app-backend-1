"""Employee Service"""

from database import AsyncSession
from models.employee import Employee
from employees.repo import (
    create,
    search,
    find_all,
    find_by_id,
    update_by_id,
    delete_by_id,
)
from employees.repo import (
    add_department_link,
    remove_department_link,
    remove_address_link,
)
from exceptions import BadRequestException, NotFoundException
from employees.schemas import CreateEmployeeRequest, UpdateEmployeeRequest
from auth.utils import hash_password

# Mainly manage business logics


async def create_employee(db: AsyncSession, data: CreateEmployeeRequest) -> Employee:
    hashed = hash_password(data.pswd)
    address_dict = data.address.model_dump() if data.address else None

    employee = await create(
        db,
        data.name,
        data.email,
        data.age,
        password_hash=hashed,
        address_data=address_dict,
    )

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
        raise NotFoundException(f"employee {id} not found")

    return employee


async def update_employee(
    db: AsyncSession, id: int, data: UpdateEmployeeRequest
) -> Employee:

    updated_fields = data.model_dump(exclude_none=True)

    if not updated_fields:
        raise BadRequestException(
            "No modified tracking properties found inside request body"
        )
    await employee_by_id(db, id)
    updated_employee = await update_by_id(db, id, updated_data=updated_fields)

    return updated_employee


async def delete_employee(db: AsyncSession, id: int) -> Employee:
    await employee_by_id(db, id)
    return await delete_by_id(db, id)


async def attach_department_to_employee(
    db: AsyncSession, employee_id: int, department_id: int
) -> None:
    await employee_by_id(db, employee_id)  # Verify existence
    await add_department_link(db, employee_id, department_id)


async def detach_employee_from_department(
    db: AsyncSession, employee_id: int, department_id: int
) -> None:
    await employee_by_id(db, employee_id)  # Verify existence
    await remove_department_link(db, employee_id, department_id)


async def delete_employee_address(
    db: AsyncSession, employee_id: int, address_id: int
) -> None:
    await employee_by_id(db, employee_id)  # Verify existence
    await remove_address_link(db, employee_id, address_id)
