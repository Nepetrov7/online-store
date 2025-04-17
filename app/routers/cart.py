from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.cart_schemas import CartCreate, CartItem, CartList, CartUpdate
from app.services.cart_service import CartService
from app.utils.dependencies import get_current_user, get_db

router = APIRouter()


def get_cart_service(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> CartService:
    return CartService(db, current_user.id)


@router.get("/", response_model=CartList)
def list_cart(
    service: CartService = Depends(get_cart_service),
):
    items = service.list_items()
    return {"items": items}


@router.post("/", response_model=CartItem, status_code=status.HTTP_201_CREATED)
def create_cart_item(
    data: CartCreate,
    service: CartService = Depends(get_cart_service),
):
    return service.add_item(data)


@router.put("/{item_id}", response_model=CartItem)
def modify_cart_item(
    item_id: int,
    data: CartUpdate,
    service: CartService = Depends(get_cart_service),
):
    item = service.update_item(item_id, data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(
    item_id: int,
    service: CartService = Depends(get_cart_service),
):
    if not service.remove_item(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_cart_items(
    service: CartService = Depends(get_cart_service),
):
    service.clear()
