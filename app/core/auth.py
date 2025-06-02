from datetime import datetime, timedelta
from typing import Optional

from fastapi import Cookie, HTTPException, Response, status
from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(subject: int, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )


def delete_auth_cookie(response: Response) -> None:
    response.delete_cookie(key="access_token", path="/")


def get_token_from_cookie(access_token: Optional[str] = Cookie(None)) -> str:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return access_token


def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        ) 