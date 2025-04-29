from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    async def get_by_category(
        self, db: AsyncSession, *, category: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        result = await db.execute(
            select(Product)
            .filter(Product.category == category)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search(
        self, db: AsyncSession, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        result = await db.execute(
            select(Product)
            .filter(Product.name.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_seller(
        self, db: AsyncSession, *, seller_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        result = await db.execute(
            select(Product)
            .filter(Product.seller_id == seller_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


product = CRUDProduct(Product) 