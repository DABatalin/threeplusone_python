from pydantic import BaseModel, Field


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemInDBBase(CartItemBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class CartItem(CartItemInDBBase):
    pass


class CartItemInDB(CartItemInDBBase):
    pass 