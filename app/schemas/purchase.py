from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class PurchaseItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price_at_time: Decimal


class PurchaseItemCreate(PurchaseItemBase):
    pass


class PurchaseItemInDBBase(PurchaseItemBase):
    id: int
    purchase_id: int

    class Config:
        from_attributes = True


class PurchaseItem(PurchaseItemInDBBase):
    pass


class PurchaseBase(BaseModel):
    total_amount: Decimal = Field(..., ge=0)


class PurchaseCreate(PurchaseBase):
    items: List[PurchaseItemCreate]


class PurchaseInDBBase(PurchaseBase):
    id: int
    user_id: int
    created_at: datetime
    items: List[PurchaseItem]

    class Config:
        from_attributes = True


class Purchase(PurchaseInDBBase):
    pass 