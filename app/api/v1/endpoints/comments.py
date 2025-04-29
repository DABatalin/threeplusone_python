from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.crud.crud_comment import comment
from app.crud.crud_product import product
from app.db.session import get_db
from app.models.user import User
from app.schemas.comment import Comment, CommentCreate, CommentUpdate

router = APIRouter()


@router.get("/product/{product_id}", response_model=List[Comment])
async def read_comments(
    *,
    db: AsyncSession = Depends(get_db),
    product_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    product_obj = await product.get(db, id=product_id)
    if not product_obj:
        raise HTTPException(status_code=404, detail="Product not found")
    comments = await comment.get_by_product(
        db, product_id=product_id, skip=skip, limit=limit
    )
    return comments


@router.post("/", response_model=Comment)
async def create_comment(
    *,
    db: AsyncSession = Depends(get_db),
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    product_obj = await product.get(db, id=comment_in.product_id)
    if not product_obj:
        raise HTTPException(status_code=404, detail="Product not found")
    comment_obj = await comment.create_with_user(
        db, obj_in=comment_in, user_id=current_user.id
    )
    return comment_obj


@router.put("/{id}", response_model=Comment)
async def update_comment(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    comment_in: CommentUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    comment_obj = await comment.get(db, id=id)
    if not comment_obj:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment_obj = await comment.update(
        db, db_obj=comment_obj, obj_in=comment_in
    )
    return comment_obj


@router.delete("/{id}", response_model=Comment)
async def delete_comment(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    comment_obj = await comment.get(db, id=id)
    if not comment_obj:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment_obj = await comment.remove(db, id=id)
    return comment_obj 