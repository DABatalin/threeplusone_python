from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token, delete_auth_cookie, set_auth_cookie
from app.core.config import settings
from app.crud.crud_user import user
from app.db.session import get_db
from app.schemas.auth import LoginRequest, LoginResponse, LogoutResponse
from app.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/register", response_model=User)
async def register(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
    response: Response,
) -> Any:
    """
    Register new user and set auth cookie.
    """
    db_user = await user.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    
    new_user = await user.create(db, obj_in=user_in)
    access_token = create_access_token(new_user.id)
    set_auth_cookie(response, access_token)
    
    return new_user


@router.post("/login", response_model=LoginResponse)
async def login(
    *,
    db: AsyncSession = Depends(get_db),
    login_in: LoginRequest,
    response: Response,
) -> Any:
    db_user = await user.authenticate(
        db, email=login_in.email, password=login_in.password
    )
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    elif not user.is_active(db_user):
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        db_user.id, expires_delta=access_token_expires
    )
    set_auth_cookie(response, access_token)
    
    return {"access_token": access_token}


@router.post("/logout", response_model=LogoutResponse)
async def logout(response: Response) -> Any:
    delete_auth_cookie(response)
    return {"message": "Successfully logged out"} 