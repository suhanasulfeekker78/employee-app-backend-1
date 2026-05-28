

from database import AsyncSession
from departments.repo import create, find_all, update_by_id
from models.department import Department

async def create_department(db:AsyncSession,  data: dict) -> Department:

    valid_datas = {}

    if data is not None and data.get("name"):
        name = data.get("name")
        if isinstance(name, str):
            valid_datas["name"] = name.strip()


    return await create(db, valid_datas)    


async def update_department(db:AsyncSession, id: int, data: dict) -> Department:

    valid_datas = {}

    if data is not None and data.get("name"):
        name = data.get("name")
        if isinstance(name, str):
            valid_datas["name"] = name.strip()


    return (await update_by_id(db, id, valid_datas))  


async def list_all_department(db:AsyncSession):
    return (await find_all(db))  

