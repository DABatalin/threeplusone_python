from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    text: str
    rating: Optional[int] = Field(None, ge=1, le=5)


class CommentCreate(CommentBase):
    product_id: int


class CommentUpdate(CommentBase):
    pass


class CommentInDBBase(CommentBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Comment(CommentInDBBase):
    pass


class CommentInDB(CommentInDBBase):
    pass 