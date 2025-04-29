from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_superuser, get_current_user
from app.crud.crud_product import product
from app.db.session import get_db
from app.models.user import User
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter()


@router.get("/", response_model=List[Product])
async def read_products(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    search: str = None,
) -> Any:
    if category:
        products = await product.get_by_category(
            db, category=category, skip=skip, limit=limit
        )
    elif search:
        products = await product.search(
            db, query=search, skip=skip, limit=limit
        )
    else:
        products = await product.get_multi(db, skip=skip, limit=limit)
    return products


@router.post("/", response_model=Product)
async def create_product(
    *,
    db: AsyncSession = Depends(get_db),
    product_in: ProductCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    product_obj = await product.create(db, obj_in=product_in)
    return product_obj


@router.get("/{id}", response_model=Product)
async def read_product(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    product_obj = await product.get(db, id=id)
    if not product_obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_obj


@router.put("/{id}", response_model=Product)
async def update_product(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    product_in: ProductUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    product_obj = await product.get(db, id=id)
    if not product_obj:
        raise HTTPException(status_code=404, detail="Product not found")
    product_obj = await product.update(db, db_obj=product_obj, obj_in=product_in)
    return product_obj


@router.delete("/{id}", response_model=Product)
async def delete_product(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    product_obj = await product.get(db, id=id)
    if not product_obj:
        raise HTTPException(status_code=404, detail="Product not found")
    product_obj = await product.remove(db, id=id)
    return product_obj 