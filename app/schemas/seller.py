from typing import Optional

from pydantic import BaseModel, Field


class SellerBase(BaseModel):
    name: str
    description: Optional[str] = None
    rating: float = Field(default=0.0, ge=0.0, le=5.0)


class SellerCreate(SellerBase):
    pass


class SellerUpdate(SellerBase):
    name: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)


class SellerInDBBase(SellerBase):
    id: int

    class Config:
        from_attributes = True


class Seller(SellerInDBBase):
    pass


class SellerInDB(SellerInDBBase):
    pass 