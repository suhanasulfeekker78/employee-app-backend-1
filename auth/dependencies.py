from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from auth.schemas import TokenPayload
from auth.utils import decode_access_token
from exceptions import UnauthorizedException
from models.employee import EmployeeRole
from exceptions import ForbiddenException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    payload=decode_access_token(token)
    if payload is None:
        raise UnauthorizedException("Invalid or expired token")
    return TokenPayload(**payload)

def require_role(*roles:EmployeeRole):
    """Return dependency that checks the user has one of the given roles."""

    def role_checker(
            current_user: TokenPayload = Depends(get_current_user)
    ) -> TokenPayload:
        if current_user.role not in roles:
            raise ForbiddenException("You do not have permission to perform this action")
        return current_user
    
    return role_checker