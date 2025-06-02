from typing import List, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.elasticsearch import elasticsearch_service


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
        self, db: AsyncSession, *, query: str, category: str = None, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        es_results = await elasticsearch_service.search_products(query, category)
        product_ids = [int(hit['_id']) for hit in es_results]
        
        if not product_ids:
            return []
        
        result = await db.execute(
            select(Product)
            .filter(Product.id.in_(product_ids))
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

    async def create(self, db: AsyncSession, *, obj_in: ProductCreate) -> Product:
        obj_in_data = obj_in.model_dump()
        db_obj = Product(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        
        result = await db.execute(
            select(Product)
            .options(selectinload(Product.comments))
            .filter(Product.id == db_obj.id)
        )
        product_with_comments = result.scalar_one()
        
        await elasticsearch_service.index_product(self._to_es_doc(product_with_comments))
        return product_with_comments

    async def update(
        self, db: AsyncSession, *, db_obj: Product, obj_in: Dict[str, Any]
    ) -> Product:
        product = await super().update(db, db_obj=db_obj, obj_in=obj_in)
        result = await db.execute(
            select(Product)
            .options(selectinload(Product.comments))
            .filter(Product.id == product.id)
        )
        product_with_comments = result.scalar_one()
        await elasticsearch_service.update_product(product.id, self._to_es_doc(product_with_comments))
        return product_with_comments

    async def remove(self, db: AsyncSession, *, id: int) -> Product:
        product = await super().remove(db, id=id)
        await elasticsearch_service.delete_product(id)
        return product

    def _to_es_doc(self, product: Product) -> dict:
        return {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'seller_id': product.seller_id,
            'comments': [
                {
                    'id': comment.id,
                    'text': comment.text,
                    'rating': comment.rating,
                    'user_id': comment.user_id
                }
                for comment in (product.comments or [])
            ]
        }


product = CRUDProduct(Product) 