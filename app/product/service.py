from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.product.model import Product
from app.product.repository import ProductRepository
from app.product.schema import ProductBase
from app.promotional.repository import PromotionalRepository
from app.utils.calculate_final_price import calculate_final_price


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)
        self.promo_repo = PromotionalRepository(db)

    @staticmethod
    def _to_date(dt):
        """
        Преобразует datetime или date в date для сравнения.
        """
        from datetime import date as _date_cls
        from datetime import datetime as _dt_cls

        if isinstance(dt, _dt_cls):
            return dt.date()
        if isinstance(dt, _date_cls):
            return dt
        return dt

    def list_products(self) -> List[Product]:
        """
        Возвращает все продукты с рассчитанной final_price
        на основе самой последней не истекшей акции.
        """
        products = self.repo.get_all()
        today = datetime.now(timezone.utc).date()
        all_promos = self.promo_repo.get_all()
        # Выбираем промо, у которых end_date >= сегодня
        active = [pr for pr in all_promos if self._to_date(pr.end_date) >= today]
        # Берем только самую новую по id
        if active:
            latest = max(active, key=lambda pr: pr.id)
            applicable = [latest]
        else:
            applicable = []
        for p in products:
            p.final_price = calculate_final_price(p, applicable)
        return products

    def get_product(self, product_id: int) -> Optional[Product]:
        """
        Возвращает продукт по ID с рассчитанной final_price
        по самой последней не истекшей акции.
        """
        p = self.repo.get_by_id(product_id)
        if p:
            today = datetime.now(timezone.utc).date()
            all_promos = self.promo_repo.get_all()
            active = [pr for pr in all_promos if self._to_date(pr.end_date) >= today]
            if active:
                latest = max(active, key=lambda pr: pr.id)
                p.final_price = calculate_final_price(p, [latest])
            else:
                p.final_price = float(p.price)
        return p

    def create_product(self, data: ProductBase) -> Product:
        prod = Product(**data.model_dump())
        return self.repo.create(prod)

    def update_product(self, product_id: int, data: ProductBase) -> Optional[Product]:
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
