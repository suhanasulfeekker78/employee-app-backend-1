from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import AsyncSession

from auth import service as auth_service
from auth.schemas import TokenResponse, RefreshTokenRequest
from database import get_db

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    token = await auth_service.login(db, form.username, form.password)
    logger.info(f"User {form.username} logged in successfully")
    return token


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshTokenRequest):
    new_tokens = await auth_service.refresh_access_token(body.refresh_token)
    return new_tokens
