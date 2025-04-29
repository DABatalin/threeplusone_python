from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.crud.crud_cart import cart
from app.crud.crud_product import product
from app.db.session import get_db
from app.models.user import User
from app.schemas.cart import CartItem, CartItemCreate, CartItemUpdate

router = APIRouter()


@router.get("/", response_model=List[CartItem])
async def read_cart_items(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    items = await cart.get_by_user(db, user_id=current_user.id)
    return items


@router.post("/", response_model=CartItem)
async def add_to_cart(
    *,
    db: AsyncSession = Depends(get_db),
    item_in: CartItemCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    product_obj = await product.get(db, id=item_in.product_id)
    if not product_obj:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_item = await cart.get_item(
        db, user_id=current_user.id, product_id=item_in.product_id
    )
    if existing_item:
        raise HTTPException(
            status_code=400,
            detail="Item already in cart. Use PUT to update quantity.",
        )
    
    db_obj = {
        "product_id": item_in.product_id,
        "quantity": item_in.quantity,
        "user_id": current_user.id
    }
    item = await cart.create(db, obj_in=db_obj)
    return item


@router.put("/{product_id}", response_model=CartItem)
async def update_cart_item(
    *,
    db: AsyncSession = Depends(get_db),
    product_id: int,
    item_in: CartItemUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    item = await cart.get_item(
        db, user_id=current_user.id, product_id=product_id
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    item = await cart.update(db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{product_id}", response_model=CartItem)
async def remove_from_cart(
    *,
    db: AsyncSession = Depends(get_db),
    product_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    item = await cart.get_item(
        db, user_id=current_user.id, product_id=product_id
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    item = await cart.remove(db, id=item.id)
    return item 