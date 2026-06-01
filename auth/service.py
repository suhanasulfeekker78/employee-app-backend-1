from database import AsyncSession
from employees import repo as employee_repo
from auth.utils import verify_password
from exceptions import UnauthorizedException
from auth.utils import create_access_token
from auth.utils import create_refresh_token, decode_refresh_token


async def login(db: AsyncSession, email: str, password: str) -> str:
    employee = await employee_repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")

    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    token_data = {
        "id": employee.id,
        "email": employee.email,
        "role": employee.role.value,
    }
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
    }


async def refresh_access_token(refresh_token: str) -> dict:
    payload = decode_refresh_token(refresh_token)
    if payload is None:
        raise UnauthorizedException("Invalid or expired refresh token")

    token_data = {
        "id": payload.get("id"),
        "email": payload.get("email"),
        "role": payload.get("role"),
    }
    new_access_token = create_access_token(token_data)

    return {"access_token": new_access_token, "refresh_token": refresh_token}
