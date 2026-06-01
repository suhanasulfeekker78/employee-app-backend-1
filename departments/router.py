from fastapi import APIRouter, Depends, status

from database import AsyncSession, get_db
from departments import service as department_service
from auth.schemas import TokenPayload
from auth.dependencies import get_current_user
from departments.schemas import (
    CreateDepartmentRequest,
    UpdateDepartmentRequest,
    DepartmentResponse,
    DepartmentDetailResponse,
)

router = APIRouter(prefix="/department", tags=["Departments"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DepartmentResponse)
async def create_department(
    body: CreateDepartmentRequest,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_service.create_department(db, body)


@router.put("/{id}", response_model=DepartmentResponse)
async def update_department(
    id: int,
    data: UpdateDepartmentRequest,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_service.update_department(db, id, data)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[DepartmentResponse])
async def list_all_department(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_service.list_all_department(db)


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=DepartmentDetailResponse
)
async def get_department_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_service.get_department_by_id(db, id)


@router.delete("/{id}", response_model=DepartmentResponse)
async def delete_department(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_service.delete_department(db, id)
