from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Optional, List
from app.repository.product_repository import ProductRepository
from app.utils.db import get_db
from app.models.product_models import Product
from app.schemas.product_schemas import ProductCreate, ProductOut

router = APIRouter()

@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
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
            status_code=400,
            detail="Рейтинг товара должен быть от 0 до 5"
        )

    new_product = repo.create_product(
        name=product.name,
        category_id=product.category_id,
        price=product.price,
        rating=product.rating,
        description=product.description
    )

    return new_product

@router.get("/", response_model=List[ProductOut])
def get_products_by_category(
    category_id: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    repo = ProductRepository(db)
    return repo.get_products_by_category(category_id, min_price, max_price, limit, offset)

@router.get("/{product_id}", response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.get_product_by_id(product_id)

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
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    for key, value in updated_data.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

# products.py

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    repo = ProductRepository(db)
    success = repo.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return {"detail": "Товар успешно удалён"}

