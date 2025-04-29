from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate, CartItemUpdate


class CRUDCart(CRUDBase[CartItem, CartItemCreate, CartItemUpdate]):
    async def get_by_user(
        self, db: AsyncSession, *, user_id: int
    ) -> List[CartItem]:
        result = await db.execute(
            select(CartItem).filter(CartItem.user_id == user_id)
        )
        return result.scalars().all()

    async def get_item(
        self, db: AsyncSession, *, user_id: int, product_id: int
    ) -> CartItem:
        result = await db.execute(
            select(CartItem).filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            )
        )
        return result.scalar_one_or_none()


cart = CRUDCart(CartItem) 