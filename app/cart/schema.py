from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CartBase(BaseModel):
    product_id: int
    quantity: Optional[int] = 1


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    quantity: int


class CartItem(CartBase):
    id: int
    user_id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True


class CartList(BaseModel):
    items: List[CartItem]
