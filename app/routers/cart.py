from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.cart_schemas import CartCreate, CartItem, CartList, CartUpdate
from app.services.cart_service import (
    add_to_cart,
    clear_cart,
    get_cart_items,
    remove_cart_item,
    update_cart_item,
)
from app.utils.dependencies import get_current_user, get_db

router = APIRouter()


@router.get("/", response_model=CartList)
def list_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    items = get_cart_items(db, current_user.id)
    return {"items": items}


@router.post("/", response_model=CartItem, status_code=status.HTTP_201_CREATED)
def create_cart_item(
    data: CartCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return add_to_cart(db, current_user.id, data)


@router.put("/{item_id}", response_model=CartItem)
def modify_cart_item(
    item_id: int,
    data: CartUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    item = update_cart_item(db, item_id, current_user.id, data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not remove_cart_item(db, item_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_cart_items(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    clear_cart(db, current_user.id)
