from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.crud.crud_cart import cart
from app.crud.crud_product import product
from app.crud.crud_purchase import purchase
from app.db.session import get_db
from app.models.user import User
from app.schemas.purchase import Purchase, PurchaseCreate, PurchaseItemCreate

router = APIRouter()


@router.get("/", response_model=List[Purchase])
async def read_purchases(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    purchases = await purchase.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return purchases


@router.post("/checkout", response_model=Purchase)
async def create_purchase(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    cart_items = await cart.get_by_user(db, user_id=current_user.id)
    if not cart_items:
        raise HTTPException(
            status_code=400, detail="No items in cart"
        )

    total_amount = 0
    purchase_items = []

    for cart_item in cart_items:
        product_obj = await product.get(db, id=cart_item.product_id)
        if not product_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Product {cart_item.product_id} not found"
            )
        if product_obj.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product_obj.name}"
            )

        total_amount += product_obj.price * cart_item.quantity
        purchase_items.append(
            PurchaseItemCreate(
                product_id=product_obj.id,
                quantity=cart_item.quantity,
                price_at_time=product_obj.price,
            )
        )

        product_obj.stock -= cart_item.quantity
        await product.update(
            db,
            db_obj=product_obj,
            obj_in={"stock": product_obj.stock}
        )
        await cart.remove(db, id=cart_item.id)

    purchase_in = PurchaseCreate(
        total_amount=total_amount,
        items=purchase_items,
    )
    purchase_obj = await purchase.create_with_items(
        db, obj_in=purchase_in, user_id=current_user.id
    )
    return purchase_obj


@router.get("/{id}", response_model=Purchase)
async def read_purchase(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    purchase_obj = await purchase.get(db, id=id)
    if not purchase_obj:
        raise HTTPException(status_code=404, detail="Purchase not found")
    if purchase_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return purchase_obj 