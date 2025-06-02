from typing import Any, List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_superuser, get_current_user
from app.crud.crud_product import product
from app.db.session import get_db
from app.models.user import User
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.services.s3 import s3_service

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


@router.post("/{id}/image", response_model=Product)
async def upload_product_image(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Upload an image for a specific product
    """
    product_obj = await product.get(db, id=id)
    if not product_obj:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
    object_name = f"products/{id}/{uuid4()}.{file_extension}"
    
    if product_obj.image_url:
        try:
            old_object_name = product_obj.image_url.split("/")[-1]
            s3_service.delete_file(f"products/{id}/{old_object_name}")
        except Exception:
            pass  

    content_type = file.content_type or "application/octet-stream"
    image_url = await s3_service.upload_file(file, object_name, content_type)

    product_obj = await product.update(
        db, 
        db_obj=product_obj, 
        obj_in=ProductUpdate(image_url=image_url)
    )
    
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

    if product_obj.image_url:
        try:
            object_name = product_obj.image_url.split("/")[-1]
            s3_service.delete_file(f"products/{id}/{object_name}")
        except Exception:
            pass  
    
    product_obj = await product.remove(db, id=id)
    return product_obj 