from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.comment import Comment
from app.models.product import Product
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.elasticsearch import elasticsearch_service


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    async def get_by_product(
        self, db: AsyncSession, *, product_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        result = await db.execute(
            select(Comment)
            .filter(Comment.product_id == product_id)
            .order_by(Comment.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_with_user(
        self, db: AsyncSession, *, obj_in: CommentCreate, user_id: int
    ) -> Comment:
        db_obj = Comment(
            **obj_in.model_dump(),
            user_id=user_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        await self._update_product_es(db, db_obj.product_id)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Comment, obj_in: CommentUpdate
    ) -> Comment:
        comment = await super().update(db, db_obj=db_obj, obj_in=obj_in)
        await self._update_product_es(db, comment.product_id)
        return comment

    async def remove(self, db: AsyncSession, *, id: int) -> Comment:
        comment = await super().remove(db, id=id)
        await self._update_product_es(db, comment.product_id)
        return comment

    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        result = await db.execute(
            select(Comment)
            .filter(Comment.user_id == user_id)
            .order_by(Comment.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def _update_product_es(self, db: AsyncSession, product_id: int):
        result = await db.execute(
            select(Product)
            .filter(Product.id == product_id)
            .options(selectinload(Product.comments))
        )
        product = result.scalar_one_or_none()
        if product:
            product_doc = {
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
                    for comment in product.comments
                ]
            }
            await elasticsearch_service.update_product(product.id, product_doc)


comment = CRUDComment(Comment) 