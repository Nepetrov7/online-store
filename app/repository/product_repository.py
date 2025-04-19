from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.product_models import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.session = db

    def get_all(self) -> List[Product]:
        return self.session.query(Product).all()

    def get_by_category(self, category_id: int) -> List[Product]:
        return (
            self.session.query(Product).filter(Product.category_id == category_id).all()
        )

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.query(Product).filter(Product.id == product_id).first()

    def create(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.commit()
