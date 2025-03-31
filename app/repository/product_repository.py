from sqlalchemy.orm import Session
from app.models.product_models import Product
from typing import Optional

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_product(self, name: str, category_id: int, price: float, rating: float, description: str) -> Product:
        product = Product(
            name=name,
            category_id=category_id,
            price=price,
            rating=rating,
            description=description,
        )
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_product_by_name(self, product_name: str) -> Optional[Product]:
        return (
            self.session.query(Product)
            .filter(Product.name.like(f"%{product_name}%"))
            .all()
        )

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.query(Product).filter(Product.id == product_id).first()

    def get_products_by_category(self, category_id: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None, limit: int = 10, offset: int = 0) -> Optional[Product]:
        query = self.session.query(Product)
        if category_id:
            query = query.filter(Product.category_id == category_id)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        return query.offset(offset).limit(limit).all()
    

    def delete_product(self, product_id: int) -> bool:
        product = self.session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False
        self.session.delete(product)
        self.session.commit()
        return True

