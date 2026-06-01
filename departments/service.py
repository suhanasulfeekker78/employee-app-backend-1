from database import AsyncSession
from departments import repo as department_repo
from models.department import Department
from departments.schemas import CreateDepartmentRequest, UpdateDepartmentRequest
from exceptions import NotFoundException


async def create_department(
    db: AsyncSession, body: CreateDepartmentRequest
) -> Department:

    return await department_repo.create(db, {"name": body.name})


async def update_department(
    db: AsyncSession, id: int, data: UpdateDepartmentRequest
) -> Department:
    return await department_repo.update_by_id(db, id, {"name": data.name})


async def list_all_department(db: AsyncSession) -> list[Department]:
    return await department_repo.find_all(db)


async def get_department_by_id(db: AsyncSession, id: int) -> Department:
    department = await department_repo.find_by_id(db, id)
    if department is None:
        raise NotFoundException("Department not found")
    return department


async def delete_department(db: AsyncSession, id: int) -> Department:
    return await department_repo.delete_by_id(db, id)
