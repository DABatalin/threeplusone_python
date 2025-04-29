from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


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
        return db_obj

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


comment = CRUDComment(Comment) 