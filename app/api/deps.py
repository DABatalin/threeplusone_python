from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_token_from_cookie, verify_token
from app.crud.crud_user import user
from app.db.session import get_db
from app.models.user import User


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token_from_cookie)
) -> User:
    user_id = verify_token(token)
    current_user = await user.get(db, id=user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user 