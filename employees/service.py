"""Employee Service"""

from database import AsyncSession
from models.employee import Employee
from models.address import Address
from employees.repo import (
    create,
    search,
    find_all,
    find_by_id,
    update_by_id,
    delete_by_id,
    add_address,
)
from employees.repo import (
    add_department_link,
    remove_department_link,
    remove_address_link,
)
from exceptions import BadRequestException, NotFoundException
from employees.schemas import (
    CreateAddressInput,
    CreateEmployeeRequest,
    UpdateEmployeeRequest,
)
from auth.utils import hash_password

# Mainly manage business logics


async def create_employee(db: AsyncSession, data: CreateEmployeeRequest) -> Employee:
    hashed = hash_password(data.pswd)
    address_dict = data.address.model_dump() if data.address else None

    employee = await create(
        db,
        data.name,
        data.email,
        data.role,
        data.status,
        data.experience,
        joining_date=data.joiningDate,
        password_hash=hashed,
        address_data=address_dict,
    )

    return employee


async def list_employee(db: AsyncSession) -> list[Employee]:
    return await find_all(db)


async def search_employee(db: AsyncSession, name: str) -> list[Employee]:

    return await search(db, name)


async def employee_by_id(db: AsyncSession, id: int) -> Employee:

    employee = await find_by_id(db, id)

    if employee is None:
        raise NotFoundException(f"employee {id} not found")

    return employee


async def update_employee(
    db: AsyncSession, id: int, data: UpdateEmployeeRequest
) -> Employee:

    updated_fields = data.model_dump(exclude_unset=True)

    if not updated_fields:
        raise BadRequestException(
            "No modified tracking properties found inside request body"
        )
    return await update_by_id(db, id, updated_data=updated_fields)


async def delete_employee(db: AsyncSession, id: int) -> Employee:
    return await delete_by_id(db, id)


async def attach_department_to_employee(
    db: AsyncSession, employee_id: int, department_id: int
) -> None:
    await add_department_link(db, employee_id, department_id)


async def detach_employee_from_department(
    db: AsyncSession, employee_id: int, department_id: int
) -> None:
    await remove_department_link(db, employee_id, department_id)


async def delete_employee_address(
    db: AsyncSession, employee_id: int, address_id: int
) -> None:
    await remove_address_link(db, employee_id, address_id)


async def add_employee_address(
    db: AsyncSession, employee_id: int, body: CreateAddressInput
) -> Address:
    address_dict = body.model_dump()
    return await add_address(db, employee_id, address_dict)
