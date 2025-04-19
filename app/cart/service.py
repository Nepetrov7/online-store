from typing import List, Optional

from sqlalchemy.orm import Session

from app.cart.model import Cart
from app.cart.repository import CartRepository
from app.cart.schema import CartCreate, CartUpdate


class CartService:
    def __init__(self, db: Session, user_id: int):
        self.user_id = user_id
        self.repo = CartRepository(db)

    def list_items(self) -> List[Cart]:
        return self.repo.list(self.user_id)

    def get_item(self, item_id: int) -> Optional[Cart]:
        return self.repo.get(item_id, self.user_id)

    def add_item(self, data: CartCreate) -> Cart:
        existing = self.repo.get_by_product(self.user_id, data.product_id)
        if existing:
            existing.quantity += data.quantity or 1
            return self.repo.update(existing)
        new_item = Cart(user_id=self.user_id, **data.model_dump())
        return self.repo.create(new_item)

    def update_item(self, item_id: int, data: CartUpdate) -> Optional[Cart]:
        item = self.repo.get(item_id, self.user_id)
        if not item:
            return None
        item.quantity = data.quantity
        return self.repo.update(item)

    def remove_item(self, item_id: int) -> bool:
        item = self.repo.get(item_id, self.user_id)
        if not item:
            return False
        self.repo.delete(item)
        return True

    def clear(self) -> None:
        self.repo.delete_all(self.user_id)
