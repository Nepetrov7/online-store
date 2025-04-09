from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.repository.product_repository import ProductRepository
from app.repository.promotional_repository import PromotionalRepository
from app.schemas.product_schemas import ProductCreate, ProductOut
from app.services.pricing_service import calculate_final_price
from app.utils.db import get_db
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=ProductOut)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = ProductRepository(db)
    # existing = repo.get_product_by_name(product.name)
    # # Валидация под вопросом
    # if existing:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Товар с таким названием уже существует"
    #     )

    if product.rating >= 0 and product.rating > 5:
        raise HTTPException(
            status_code=400, detail="Рейтинг товара должен быть от 0 до 5"
        )

    new_product = repo.create_product(
        name=product.name,
        category_id=product.category_id,
        price=product.price,
        rating=product.rating,
        description=product.description,
    )

    return new_product


@router.get("/", response_model=List[ProductOut])
def get_products_by_category(
    category_id: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    repo = ProductRepository(db)
    return repo.get_products_by_category(
        category_id, min_price, max_price, limit, offset
    )


@router.get("/{product_id}", response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    promo_repo = PromotionalRepository(db)

    product = product_repo.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Получаем активные промоакции для данного продукта
    active_promos = promo_repo.get_active_promotions_for_product(product_id)
    # Вычисляем финальную цену
    final_price = calculate_final_price(product, active_promos)

    setattr(product, "final_price", final_price)

    return product


@router.get("/name/{product_name}", response_model=List[ProductOut])
def get_product_by_name(
    product_name: str,
    db: Session = Depends(get_db),
):
    repo = ProductRepository(db)
    return repo.get_product_by_name(product_name)


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    updated_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = ProductRepository(db)
    product = repo.update_product(product_id, updated_data.model_dump())

    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = ProductRepository(db)
    success = repo.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return {"detail": "Товар успешно удалён"}
