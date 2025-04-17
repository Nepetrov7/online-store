from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.cart_models import Cart
from app.repository.cart_repository import CartRepository
from app.schemas.cart_schemas import CartCreate, CartUpdate


def get_cart_items(db: Session, user_id: int) -> List[Cart]:
    repo = CartRepository(db)
    return repo.list(user_id)


def get_cart_item(db: Session, item_id: int, user_id: int) -> Optional[Cart]:
    repo = CartRepository(db)
    return repo.get(item_id, user_id)


def add_to_cart(db: Session, user_id: int, data: CartCreate) -> Cart:
    repo = CartRepository(db)
    existing = repo.get_by_product(user_id, data.product_id)
    if existing:
        existing.quantity += data.quantity or 1
        repo.update(existing)
        return existing

    new_item = Cart(user_id=user_id, **data.model_dump())
    return repo.create(new_item)


def update_cart_item(
    db: Session, item_id: int, user_id: int, data: CartUpdate
) -> Optional[Cart]:
    repo = CartRepository(db)
    item = repo.get(item_id, user_id)
    if not item:
        return None
    item.quantity = data.quantity
    return repo.update(item)


def remove_cart_item(db: Session, item_id: int, user_id: int) -> bool:
    repo = CartRepository(db)
    item = repo.get(item_id, user_id)
    if not item:
        return False
    repo.delete(item)
    return True


def clear_cart(db: Session, user_id: int) -> None:
    repo = CartRepository(db)
    repo.delete_all(user_id)
