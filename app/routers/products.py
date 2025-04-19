from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.product_schemas import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService
from app.utils.dependencies import get_current_user, get_db

router = APIRouter()


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.get("/", response_model=List[ProductResponse])
def list_products(
    category_id: Optional[int] = None,
    service: ProductService = Depends(get_product_service),
):
    if category_id is not None:
        return service.list_by_category(category_id)
    return service.list_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    prod = service.get_product(product_id)
    if not prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return prod


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
    current_user=Depends(get_current_user),
):
    return service.create_product(data)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
    current_user=Depends(get_current_user),
):
    updated = service.update_product(product_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
    current_user=Depends(get_current_user),
):
    if not service.delete_product(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return {"detail": "Deleted"}
