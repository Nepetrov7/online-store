from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.cart_models import Cart


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, user_id: int) -> List[Cart]:
        return self.db.query(Cart).filter(Cart.user_id == user_id).all()

    def get(self, item_id: int, user_id: int) -> Optional[Cart]:
        return (
            self.db.query(Cart)
            .filter(Cart.id == item_id, Cart.user_id == user_id)
            .first()
        )

    def get_by_product(self, user_id: int, product_id: int) -> Optional[Cart]:
        return (
            self.db.query(Cart)
            .filter(Cart.user_id == user_id, Cart.product_id == product_id)
            .first()
        )

    def create(self, cart_item: Cart) -> Cart:
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def update(self, cart_item: Cart) -> Cart:
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def delete(self, cart_item: Cart) -> None:
        self.db.delete(cart_item)
        self.db.commit()

    def delete_all(self, user_id: int) -> None:
        self.db.query(Cart).filter(Cart.user_id == user_id).delete()
        self.db.commit()
