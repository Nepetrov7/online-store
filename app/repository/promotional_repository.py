from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.promotional_models import Promotional, promotion_products


class PromotionalRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_promotional(
        self,
        promotion_name: str,
        discount_type: str,
        discount_value: float,
        start_date: datetime,
        end_date: datetime,
    ) -> Promotional:
        promotional = Promotional(
            promotion_name=promotion_name,
            discount_type=discount_type,
            discount_value=discount_value,
            start_date=start_date,
            end_date=end_date,
        )
        self.session.add(promotional)
        self.session.commit()
        self.session.refresh(promotional)
        return promotional

    def add_product_to_promotion(self, promotion_id: int, product_id: int) -> None:
        # Добавляем связь между акцией и продуктом
        self.session.execute(
            "INSERT INTO promotion_products (promotion_id, product_id) VALUES "
            "(:promotion_id, :product_id)",
            {"promotion_id": promotion_id, "product_id": product_id},
        )
        self.session.commit()

    def get_active_promotions_for_product(self, product_id: int) -> List[Promotional]:
        now = datetime.now(timezone.utc)
        active_promos = (
            self.session.query(Promotional)
            .join(promotion_products)
            .filter(
                promotion_products.c.product_id == product_id,
                Promotional.start_date <= now,
                Promotional.end_date >= now,
            )
            .all()
        )
        return active_promos

    def get_all_promotional(self) -> List[Promotional]:
        return self.session.query(Promotional).all()

    def get_promotional_by_id(self, promotional_id: int) -> Optional[Promotional]:
        return (
            self.session.query(Promotional)
            .filter(Promotional.id == promotional_id)
            .first()
        )

    def delete_promotional(self, promotional_id: int) -> bool:
        promotional = (
            self.session.query(Promotional)
            .filter(Promotional.id == promotional_id)
            .first()
        )
        if not promotional:
            return False
        self.session.delete(promotional)
        self.session.commit()
        return True
