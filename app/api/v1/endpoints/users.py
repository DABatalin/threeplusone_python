from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_superuser, get_current_user
from app.crud.crud_user import user
from app.db.session import get_db
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/me", response_model=User)
async def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    user_obj = await user.update(db, db_obj=current_user, obj_in=user_in)
    return user_obj


@router.post("/", response_model=User)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    user_obj = await user.get_by_email(db, email=user_in.email)
    if user_obj:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_obj = await user.create(db, obj_in=user_in)
    return user_obj


@router.get("/{user_id}", response_model=User)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_db),
) -> Any:
    user_obj = await user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(
            status_code=404,
            detail="The user with this ID does not exist in the system",
        )
    return user_obj 