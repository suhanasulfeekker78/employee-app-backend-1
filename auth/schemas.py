from pydantic import BaseModel, EmailStr, Field

class TokenResponse(BaseModel):
    access_token:str
    refresh_token: str
    token_type:str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    """Decoded JWT payload."""
    id: int
    email: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str