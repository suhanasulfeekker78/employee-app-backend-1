from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    id: int
    email: str
    role: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
