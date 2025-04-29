from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.purchase import Purchase, PurchaseItem
from app.schemas.purchase import PurchaseCreate, PurchaseItemCreate


class CRUDPurchase(CRUDBase[Purchase, PurchaseCreate, PurchaseCreate]):
    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Purchase]:
        result = await db.execute(
            select(Purchase)
            .filter(Purchase.user_id == user_id)
            .order_by(Purchase.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_with_items(
        self, db: AsyncSession, *, obj_in: PurchaseCreate, user_id: int
    ) -> Purchase:
        db_obj = Purchase(
            user_id=user_id,
            total_amount=obj_in.total_amount,
        )
        db.add(db_obj)
        await db.flush()

        for item in obj_in.items:
            db_item = PurchaseItem(
                purchase_id=db_obj.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_time=item.price_at_time,
            )
            db.add(db_item)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj


purchase = CRUDPurchase(Purchase) 