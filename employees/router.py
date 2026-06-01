"""Employee Router"""

from fastapi import APIRouter, status, Depends
from auth.schemas import TokenPayload
from auth.dependencies import get_current_user

from database import AsyncSession, get_db

from employees import service

from employees.schemas import (
    CreateEmployeeRequest,
    CreateEmployeeResponse,
    GetEmployeeByIDResponse,
)
from employees.schemas import UpdateEmployeeRequest
from auth.dependencies import require_role
from models.employee import EmployeeRole

# Contains mainly the routes , parsing logics

router = APIRouter(prefix="/employee", tags=["Employees"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateEmployeeResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def create_employee(
    body: CreateEmployeeRequest, db: AsyncSession = Depends(get_db)
):
    employee = await service.create_employee(db, body)

    return employee


@router.get("/search", response_model=list[GetEmployeeByIDResponse])
async def search_employee(
    name: str = "",
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):

    employees = await service.search_employee(db, name)

    return employees


@router.get("", response_model=list[CreateEmployeeResponse])
async def list_employee(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):

    employees = await service.list_employee(db)

    return employees


@router.get("/{id}", response_model=GetEmployeeByIDResponse)
async def get_employee_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):

    employee = await service.employee_by_id(db, id)

    return employee


@router.put(
    "/{id}",
    response_model=GetEmployeeByIDResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def update_employee(
    id: int,
    body: UpdateEmployeeRequest,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):

    updated_employee = await service.update_employee(db, id, body)

    return updated_employee


@router.delete(
    "/{id}",
    response_model=GetEmployeeByIDResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def delete_employee(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):

    employee = await service.delete_employee(db, id)

    return employee


# TASK3
@router.post(
    "/{employee_id}/departments/{department_id}", status_code=status.HTTP_200_OK
)
async def attach_department_to_employee(
    employee_id: int,
    department_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    await service.attach_department_to_employee(db, employee_id, department_id)
    return {"detail": "Employee linked to department successfully"}


@router.delete(
    "/{employee_id}/departments/{department_id}", status_code=status.HTTP_200_OK
)
async def detach_employee_from_department(
    employee_id: int,
    department_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    await service.detach_employee_from_department(db, employee_id, department_id)
    return {"detail": "Employee unlinked from department successfully"}


@router.delete("/{employee_id}/addresses/{address_id}", status_code=status.HTTP_200_OK)
async def delete_employee_address(
    employee_id: int,
    address_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    await service.delete_employee_address(db, employee_id, address_id)
    return {"detail": "Employee address soft-deleted successfully"}
