from database import AsyncSession
from employees import repo as employee_repo
from auth.utils import verify_password
from exceptions import UnauthorizedException
from auth.utils import create_access_token

async def login(db:AsyncSession, email:str, password:str) ->str:
    employee= await employee_repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    
    return create_access_token({"id":employee.id,"email":employee.email})