from pydantic import BaseModel

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemOut(CartItemCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
