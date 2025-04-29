from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    category: str
    stock: int = Field(..., ge=0)
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    seller_id: int


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    category: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)


class ProductInDBBase(ProductBase):
    id: int
    seller_id: int

    class Config:
        from_attributes = True


class Product(ProductInDBBase):
    pass


class ProductInDB(ProductInDBBase):
    pass 