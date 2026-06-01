from fastapi import APIRouter, Depends
from database import AsyncSession

from auth import service as auth_service
from auth.schemas import LoginRequest, TokenResponse, RefreshTokenRequest
from database import get_db

router=APIRouter(prefix="/auth", tags=["Auth"])

@router.post("login", response_model=TokenResponse)
async def login(body:LoginRequest, db:AsyncSession=Depends(get_db)):
    token=await auth_service.login(db,body.email,body.password)
    return token

@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshTokenRequest):
    new_tokens = await auth_service.refresh_access_token(body.refresh_token)
    return new_tokens