from typing import List, Optional

from sqlalchemy.orm import Session

from app.product.model import Product
from app.product.repository import ProductRepository
from app.product.schema import ProductBase


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def list_products(self) -> List[Product]:
        return self.repo.get_all()

    def list_by_category(self, category_id: int) -> List[Product]:
        return self.repo.get_by_category(category_id)

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.repo.get_by_id(product_id)

    def create_product(self, data: ProductBase) -> Product:
        prod = Product(**data.model_dump())
        return self.repo.create(prod)

    def update_product(self, product_id: int, data: dict) -> Optional[Product]:
        prod = self.repo.get_by_id(product_id)
        if not prod:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(prod, field, value)
        return self.repo.update(prod)

    def delete_product(self, product_id: int) -> bool:
        prod = self.repo.get_by_id(product_id)
        if not prod:
            return False
        self.repo.delete(prod)
        return True
