from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_superuser
from app.crud.crud_seller import seller
from app.db.session import get_db
from app.schemas.seller import Seller, SellerCreate, SellerUpdate

router = APIRouter()


@router.get("/", response_model=List[Seller])
async def read_sellers(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    sellers = await seller.get_multi(db, skip=skip, limit=limit)
    return sellers


@router.post("/", response_model=Seller)
async def create_seller(
    *,
    db: AsyncSession = Depends(get_db),
    seller_in: SellerCreate,
    current_user: Any = Depends(get_current_active_superuser),
) -> Any:
    seller_obj = await seller.create(db, obj_in=seller_in)
    return seller_obj


@router.put("/{id}", response_model=Seller)
async def update_seller(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    seller_in: SellerUpdate,
    current_user: Any = Depends(get_current_active_superuser),
) -> Any:
    seller_obj = await seller.get(db, id=id)
    if not seller_obj:
        raise HTTPException(status_code=404, detail="Seller not found")
    seller_obj = await seller.update(db, db_obj=seller_obj, obj_in=seller_in)
    return seller_obj


@router.get("/{id}", response_model=Seller)
async def read_seller(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    seller_obj = await seller.get(db, id=id)
    if not seller_obj:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller_obj


@router.delete("/{id}", response_model=Seller)
async def delete_seller(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: Any = Depends(get_current_active_superuser),
) -> Any:
    seller_obj = await seller.get(db, id=id)
    if not seller_obj:
        raise HTTPException(status_code=404, detail="Seller not found")
    seller_obj = await seller.remove(db, id=id)
    return seller_obj 