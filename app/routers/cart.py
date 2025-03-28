from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.models.cart_models import CartItem
from app.models.product_models import Product
from app.schemas.cart_schemas import CartItemCreate, CartItemOut
from fastapi import Path

router = APIRouter()


def get_current_user_id():
    return 1  # позже заменим на настоящую авторизацию

@router.post("/", response_model=CartItemOut)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    cart_item = CartItem(
        user_id=user_id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.get("/", response_model=list[CartItemOut])
def get_cart(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

@router.delete("/{item_id}")
def delete_cart_item(
    item_id: int = Path(..., description="ID позиции в корзине"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Позиция в корзине не найдена")

    db.delete(cart_item)
    db.commit()
    return {"detail": "Позиция удалена из корзины"}
